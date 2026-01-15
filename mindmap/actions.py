from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Sequence, Union

import mindm
import mindmap.mindmap as mm
from mindmap import serialization

JsonValue = Union[str, int, float, bool, None, Dict[str, "JsonValue"], List["JsonValue"]]

DEFAULT_MACOS_ACCESS = "applescript"
DEFAULT_CHARTTYPE = "auto"
VALID_MODES = ("full", "content", "text")
VALID_MACOS_ACCESS = ("applescript", "appscript")
VALID_CHARTTYPES = ("auto", "orgchart", "radial")


def _serialize_result(data: Any) -> JsonValue:
    """Serialize MindmapTopic structures into JSON-friendly values.

    Args:
        data (Any): The data to serialize.

    Returns:
        JsonValue: JSON-serializable representation of the input.
    """
    if isinstance(data, (mm.MindmapTopic, list)):
        return serialization.serialize_object_simple(data)
    if isinstance(data, tuple):
        return list(data)
    if isinstance(data, (dict, str, int, float, bool)) or data is None:
        return data
    return str(data)


def _handle_mindmanager_error(func_name: str, exc: Exception) -> Dict[str, str]:
    """Format MindManager errors for CLI or skill consumers.

    Args:
        func_name (str): Function name where the error occurred.
        exc (Exception): The exception that was raised.

    Returns:
        Dict[str, str]: Standardized error payload.
    """
    if "No document found" in str(exc):
        return {
            "error": "MindManager Error",
            "message": "No document found or MindManager not running.",
        }
    return {
        "error": "MindManager Error",
        "message": f"Error during MindManager operation '{func_name}': {exc}",
    }


def _get_document_instance(
    charttype: str = DEFAULT_CHARTTYPE,
    turbo_mode: bool = False,
    macos_access: str = DEFAULT_MACOS_ACCESS,
) -> mm.MindmapDocument:
    """Create a configured MindmapDocument instance."""
    return mm.MindmapDocument(
        charttype=charttype,
        turbo_mode=turbo_mode,
        inline_editing_mode=False,
        mermaid_mode=True,
        macos_access=macos_access,
    )


def _get_document_with_mindmap(
    mode: str = "full",
    turbo_mode: bool = False,
    charttype: str = DEFAULT_CHARTTYPE,
    macos_access: str = DEFAULT_MACOS_ACCESS,
) -> Optional[mm.MindmapDocument]:
    document = _get_document_instance(
        charttype=charttype,
        turbo_mode=turbo_mode,
        macos_access=macos_access,
    )
    if document.get_mindmap(mode=mode):
        return document
    return None


def get_mindmap(
    mode: str = "full",
    turbo_mode: bool = False,
    charttype: str = DEFAULT_CHARTTYPE,
    macos_access: str = DEFAULT_MACOS_ACCESS,
) -> JsonValue:
    """Retrieve the current mindmap and serialize it.

    Args:
        mode (str): Detail level ("full", "content", "text"). (Unused for selection.)
        turbo_mode (bool): Enable turbo mode (text-only operations).
        charttype (str): Mindmap chart type (auto/orgchart/radial).
        macos_access (str): macOS MindManager access method.

    Returns:
        JsonValue: Serialized mindmap or error payload.
    """
    try:
        document = _get_document_with_mindmap(
            mode=mode,
            turbo_mode=turbo_mode,
            charttype=charttype,
            macos_access=macos_access,
        )
        if document is None:
            return {
                "error": "MindManager Error",
                "message": "No document found or MindManager not running.",
            }
        return _serialize_result(document.mindmap)
    except Exception as exc:
        return _handle_mindmanager_error("get_mindmap", exc)


def get_selection(
    mode: str = "full",
    turbo_mode: bool = False,
    charttype: str = DEFAULT_CHARTTYPE,
    macos_access: str = DEFAULT_MACOS_ACCESS,
) -> JsonValue:
    """Retrieve the currently selected topics in MindManager.

    Args:
        mode (str): Detail level ("full", "content", "text").
        turbo_mode (bool): Enable turbo mode (text-only operations).
        charttype (str): Mindmap chart type (auto/orgchart/radial).
        macos_access (str): macOS MindManager access method.

    Returns:
        JsonValue: List of serialized topics or error payload.
    """
    try:
        document = _get_document_instance(
            charttype=charttype,
            turbo_mode=turbo_mode,
            macos_access=macos_access,
        )
        selection = document.get_selection()
        return _serialize_result(selection)
    except Exception as exc:
        return _handle_mindmanager_error("get_selection", exc)


def get_grounding_information(
    mode: str = "full",
    turbo_mode: bool = False,
    charttype: str = DEFAULT_CHARTTYPE,
    macos_access: str = DEFAULT_MACOS_ACCESS,
) -> JsonValue:
    """Extract grounding information from the current mindmap.

    Args:
        mode (str): Detail level ("full", "content", "text").
        turbo_mode (bool): Enable turbo mode (text-only operations).
        charttype (str): Mindmap chart type (auto/orgchart/radial).
        macos_access (str): macOS MindManager access method.

    Returns:
        JsonValue: Dict with grounding information or error payload.
    """
    try:
        document = _get_document_with_mindmap(
            mode=mode,
            turbo_mode=turbo_mode,
            charttype=charttype,
            macos_access=macos_access,
        )
        if document is None:
            return {
                "error": "MindManager Error",
                "message": "No document found or MindManager not running.",
            }
        document.get_selection()
        top_most, subtopics = document.get_grounding_information()
        return {"top_most": top_most, "subtopics": subtopics}
    except Exception as exc:
        return {
            "error": "Internal Error",
            "message": f"Failed to get grounding information: {exc}",
        }


def get_library_folder(
    charttype: str = DEFAULT_CHARTTYPE,
    macos_access: str = DEFAULT_MACOS_ACCESS,
) -> JsonValue:
    """Get the path to the MindManager library folder.

    Args:
        charttype (str): Mindmap chart type (auto/orgchart/radial).
        macos_access (str): macOS MindManager access method.

    Returns:
        JsonValue: Folder path or error payload.
    """
    try:
        mindmanager_obj = mindm.mindmanager.Mindmanager(
            charttype=charttype, macos_access=macos_access
        )
        return mindmanager_obj.get_library_folder()
    except Exception as exc:
        return _handle_mindmanager_error("get_library_folder", exc)


def serialize_current_mindmap_to_mermaid(
    id_only: bool = False,
    mode: str = "content",
    turbo_mode: bool = False,
    charttype: str = DEFAULT_CHARTTYPE,
    macos_access: str = DEFAULT_MACOS_ACCESS,
) -> Union[str, Dict[str, str]]:
    """Serialize the current mindmap to Mermaid format.

    Args:
        id_only (bool): If True, include only IDs without attributes (full mode only).
        mode (str): Detail level ("full", "content", "text"). Full mode emits
            Mermaid with metadata comments; other modes emit simplified Mermaid.
        turbo_mode (bool): Enable turbo mode (text-only operations).
        charttype (str): Mindmap chart type (auto/orgchart/radial).
        macos_access (str): macOS MindManager access method.

    Returns:
        Union[str, Dict[str, str]]: Mermaid string or error payload.
    """
    try:
        document = _get_document_with_mindmap(
            mode=mode,
            turbo_mode=turbo_mode,
            charttype=charttype,
            macos_access=macos_access,
        )
        if document is None:
            return {
                "error": "MindManager Error",
                "message": "No document found or MindManager not running.",
            }
        if mode == "full":
            guid_mapping: Dict[str, int] = {}
            serialization.build_mapping(document.mindmap, guid_mapping)
            return serialization.serialize_mindmap(
                document.mindmap, guid_mapping, id_only=id_only
            )
        return serialization.serialize_mindmap_simple(document.mindmap)
    except Exception as exc:
        return _handle_mindmanager_error("serialize_current_mindmap_to_mermaid", exc)


def _is_full_mermaid(mermaid: str) -> bool:
    return "%%" in mermaid


def create_mindmap_from_mermaid(
    mermaid: str,
    turbo_mode: bool = False,
    charttype: str = DEFAULT_CHARTTYPE,
    macos_access: str = DEFAULT_MACOS_ACCESS,
) -> JsonValue:
    """Create a MindManager mindmap from Mermaid syntax (full or simplified).

    Args:
        mermaid (str): Mermaid mindmap text (full with metadata or simplified).
        turbo_mode (bool): Enable turbo mode (text-only operations).
        charttype (str): Mindmap chart type (auto/orgchart/radial).
        macos_access (str): macOS MindManager access method.

    Returns:
        JsonValue: Status dict or error payload.
    """
    if not mermaid or not mermaid.strip():
        return {"error": "Invalid Input", "message": "Mermaid content is required."}
    try:
        if _is_full_mermaid(mermaid):
            guid_mapping: Dict[str, int] = {}
            deserialized = serialization.deserialize_mermaid_full(mermaid, guid_mapping)
            message = "Mindmap created from Mermaid diagram."
        else:
            deserialized = serialization.deserialize_mermaid_simple(mermaid)
            message = "Mindmap created from Mermaid diagram (simple)."
        document = _get_document_instance(
            charttype=charttype,
            turbo_mode=turbo_mode,
            macos_access=macos_access,
        )
        document.mindmap = deserialized
        document.create_mindmap()
        return {"status": "success", "message": message}
    except Exception as exc:
        return _handle_mindmanager_error("create_mindmap_from_mermaid", exc)


def _json_dumps(payload: JsonValue, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(payload, indent=2)
    return json.dumps(payload)


def _add_turbo_flag(parser: argparse.ArgumentParser, default: bool = False) -> None:
    if default:
        parser.add_argument(
            "--no-turbo-mode",
            dest="turbo_mode",
            action="store_false",
            help="Disable turbo mode for this command.",
        )
        parser.set_defaults(turbo_mode=True)
    else:
        parser.add_argument(
            "--turbo-mode",
            dest="turbo_mode",
            action="store_true",
            help="Enable turbo mode (text-only operations).",
        )


def _add_common_args(
    parser: argparse.ArgumentParser,
    *,
    include_mode: bool = True,
    default_mode: str = "full",
    turbo_default: bool = False,
    include_turbo: bool = True,
) -> None:
    if include_mode:
        parser.add_argument(
            "--mode",
            default=default_mode,
            choices=VALID_MODES,
            help="Detail level for mindmap extraction.",
        )
    if include_turbo:
        _add_turbo_flag(parser, default=turbo_default)
    parser.add_argument(
        "--charttype",
        default=DEFAULT_CHARTTYPE,
        choices=VALID_CHARTTYPES,
        help="Chart type for MindManager templates.",
    )
    parser.add_argument(
        "--macos-access",
        default=DEFAULT_MACOS_ACCESS,
        choices=VALID_MACOS_ACCESS,
        help="macOS MindManager access method.",
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="High-level MindManager mindmap operations."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Force JSON output for text responses.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_get = subparsers.add_parser("get-mindmap", help="Get the mindmap.")
    _add_common_args(parser_get)

    parser_selection = subparsers.add_parser(
        "get-selection", help="Get selected topics."
    )
    _add_common_args(parser_selection)

    parser_grounding = subparsers.add_parser(
        "get-grounding-information", help="Get grounding information."
    )
    _add_common_args(parser_grounding)

    parser_library = subparsers.add_parser(
        "get-library-folder", help="Get the library folder path."
    )
    _add_common_args(parser_library, include_mode=False)

    parser_mermaid = subparsers.add_parser(
        "serialize-mermaid", help="Serialize to Mermaid format."
    )
    parser_mermaid.add_argument(
        "--id-only",
        action="store_true",
        help="Serialize Mermaid with IDs only.",
    )
    _add_common_args(parser_mermaid, default_mode="content")

    parser_create = subparsers.add_parser(
        "create-from-mermaid",
        help="Create mindmap from Mermaid (auto-detect full vs simplified).",
    )
    input_group = parser_create.add_mutually_exclusive_group()
    input_group.add_argument("--input", help="Path to Mermaid text file.")
    input_group.add_argument("--text", help="Mermaid text payload.")
    _add_common_args(parser_create, include_mode=False, include_turbo=False)
    _add_turbo_flag(parser_create, default=False)

    return parser


def _read_mermaid_input(text: Optional[str], path: Optional[str]) -> str:
    if text is not None:
        return text
    if path is not None:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    if sys.stdin.isatty():
        raise ValueError("Provide --text, --input, or pipe Mermaid via stdin.")
    return sys.stdin.read()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    result: JsonValue
    output_kind = "json"
    exit_code: Optional[int] = None

    if args.command == "get-mindmap":
        result = get_mindmap(
            mode=args.mode,
            turbo_mode=args.turbo_mode,
            charttype=args.charttype,
            macos_access=args.macos_access,
        )
    elif args.command == "get-selection":
        result = get_selection(
            mode=args.mode,
            turbo_mode=args.turbo_mode,
            charttype=args.charttype,
            macos_access=args.macos_access,
        )
    elif args.command == "get-grounding-information":
        result = get_grounding_information(
            mode=args.mode,
            turbo_mode=args.turbo_mode,
            charttype=args.charttype,
            macos_access=args.macos_access,
        )
    elif args.command == "get-library-folder":
        result = get_library_folder(
            charttype=args.charttype, macos_access=args.macos_access
        )
        output_kind = "text"
    elif args.command == "serialize-mermaid":
        result = serialize_current_mindmap_to_mermaid(
            id_only=args.id_only,
            mode=args.mode,
            turbo_mode=args.turbo_mode,
            charttype=args.charttype,
            macos_access=args.macos_access,
        )
        output_kind = "text"
    elif args.command == "create-from-mermaid":
        try:
            mermaid_text = _read_mermaid_input(args.text, args.input)
        except ValueError as exc:
            result = {"error": "Invalid Input", "message": str(exc)}
            exit_code = 2
        else:
            result = create_mindmap_from_mermaid(
                mermaid=mermaid_text,
                turbo_mode=args.turbo_mode,
                charttype=args.charttype,
                macos_access=args.macos_access,
            )
    else:
        parser.print_help()
        return 2

    is_error = isinstance(result, dict) and "error" in result
    if output_kind == "text" and not args.json and isinstance(result, str):
        sys.stdout.write(result)
    else:
        print(_json_dumps(result, pretty=args.pretty))

    if exit_code is not None:
        return exit_code
    return 1 if is_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
