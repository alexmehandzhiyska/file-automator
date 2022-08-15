from file_automator import search_main_dirs, search_sub_dirs

def test_search_main_dirs():
    assert(search_main_dirs(['hs'])) == '/Education/High School/Year 12'
    assert(search_main_dirs(['work'])) == '/Work'
    assert(search_main_dirs([])) == ''

def test_search_sub_dirs():
    assert(search_sub_dirs(['bio'])) == ['/Biology']
    assert(search_sub_dirs(['testing', 'js-apps'])) == ['/Testing', '/JS Apps Testing']
    assert(search_sub_dirs([])) == []