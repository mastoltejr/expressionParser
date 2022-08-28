from expressionParser import createExpressionTree


def test_pemdas():
    assert createExpressionTree(
        expression='1+2^2*3!-4/2+10\\3-13%7').exec()() == 20


def test_comparators():
    assert createExpressionTree(
        expression='(5*6>=20+5)==(2<=3)') == True
