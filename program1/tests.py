__author__ = 'Jai Chaudhary'
import logging
from config import EXAMPLE_DATA,F_FIELDS,S_FIELDS
from code.utils import *
logging.basicConfig(filename='logs/tests.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')


def _test_utils():
    """
    Simple tests to verify functions, data loading,
    :return:
    """
    x = numpy.array([[1,2],[3,4],[5,6],[7,8]])
    y = numpy.array([1,2,3,40])
    model = linear_regression(x,y)
    print "model coefficients",model.coef_,model.intercept_
    print y,model.predict(x)
    print metrics(model,x,y)
    #print tls(model,x,y)
    rows = [row for row in load_csv_lazy(EXAMPLE_DATA,S_FIELDS,F_FIELDS)]
    print "rows",len(rows)
    for r in rows[-30:]:
        print r

if __name__ == '__main__':
    _test_utils()

