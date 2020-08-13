from lla.interpreter import Interpreter


def test_main():
    variables = {}
    interpreter = Interpreter(variables)

    variables['ssh'] = True
    variables['website_up'] = True
    variables['search'] = False

    assert interpreter.run('!website_up | !search | ssh')

    assert interpreter.referenced_variables == {'website_up', 'search'}
    assert interpreter.last_referenced_variable == 'search'
