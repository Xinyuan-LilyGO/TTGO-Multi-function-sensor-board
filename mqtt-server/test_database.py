import database
import time
import logging
import sys
import os


# setup the logger
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def test_write_to_database_sync():

    db = database.Database()
    assert db.open("thisdoesntexist.db", threaded=False)
    assert db.is_open()
    db.write_message("mytopic_sync", "mydata_sync".encode('utf-8'))
    db.write_message("mytopic_2_sync", "mydata_sync".encode('utf-8'))
    db.close()
    assert not db.is_open()


def test_write_to_database_async():
    db = database.Database()
    assert db.open("thisdoesntexist.db", threaded=True)
    assert db.is_open()
    db.write_message("mytopic_async", "mydata_async".encode('utf-8'))
    db.write_message("mytopic_2_async", "mydata_async".encode('utf-8'))
    db.close(wait_for_write=True)
    assert not db.is_open()


def test_write_to_database_sync_and_get_topics():

    db_name = "test_write_to_database_sync_and_get_topics.db"
    db = database.Database()
    if os.path.exists(db_name):
        os.remove(db_name)
    assert db.open(db_name, threaded=False)
    assert db.is_open()
    db.write_message("b_topic", "mydata_sync".encode('utf-8'))
    db.write_message("a_topic", "mydata_sync".encode('utf-8'))

    # check that the topics are all present and ordered by the topic (alphabetical order)
    topics = db.get_topics()
    assert len(topics) == 2
    topics[0] == "a_topic"
    topics[1] == "b_topic"

    db.close()
    assert not db.is_open()


if __name__ == "__main__":
    test_write_to_database_sync()
    test_write_to_database_async()
