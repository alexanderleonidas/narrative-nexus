from utils.preprocess import Preprocess
from utils.helper import Helper


preprocess = Preprocess()
helper = Helper()

print('Preprocessing Isaac Asimov\'s The Foundation Trilogy...')
trilogy = preprocess.preprocess_asimov()
helper.save_data(trilogy, 'data/processed_asimov_clean.pkl')



