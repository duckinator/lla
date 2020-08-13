from lla.interpreter import Interpreter


def test_referenced_variables():
    variables = {}
    interpreter = Interpreter(variables)

    variables['a'] = True
    variables['b'] = True
    variables['c'] = False

    assert interpreter.run('!a | !c | b')

    assert interpreter.referenced_variables == {'a', 'c'}
    assert interpreter.last_referenced_variable == 'c'
