from utils.preprocess import Preprocess
from utils.helper import Helper
from utils.asimov import Asimov

asimov = Asimov()
preprocess = Preprocess(asimov)
helper = Helper()

print('Preprocessing Isaac Asimov\'s The Foundation Trilogy...')
trilogy = preprocess.preprocess_asimov()
helper.save_data(trilogy, 'data/processed_asimov.pkl')




