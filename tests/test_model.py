from file_storage.model import Model


def test_user(model: Model):
    model.create_user('test01', 'kjhni3j')
    assert model.get_user_id('test01', 'kjhni3j') == 1
    assert model.get_user_id('test01', 'kjhni3u') is None
