import mindm.mindmanager

def iterate_topics(topic):
    text = m.get_text_from_topic(topic)
    m.set_text_to_topic(topic, text.upper())

    subtopics = m.get_subtopics_from_topic(topic)
    for subtopic in subtopics:
        iterate_topics(subtopic)

m = mindm.mindmanager.Mindmanager()
central_topic = m.get_central_topic()
iterate_topics(central_topic)
