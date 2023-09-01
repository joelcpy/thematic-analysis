import os

from gensim.models import LdaModel
from gensim.corpora import Dictionary
import gensim.corpora as corpora

from preprocessing import preprocessing_text

class ThemePredictor:
    def __init__(self):
        """ Initialise and load model, dictionary"""

        # Navigate to the parent directory
        parent_dir = os.path.dirname(os.getcwd())
        model_path = os.path.join(parent_dir, 'models')
        # Load the LDA model
        self.loaded_lda_model = LdaModel.load(model_path + "/lda_model")
        
        # Load the dictionary
        self.loaded_dictionary = Dictionary.load(model_path + "/lda_model.id2word")
        
    
    def predict(self, text: str) -> str:
        """ 
        Initialise and load model, dictionary

        Args:
        - text:: text to be predicted
        """
        # Process text
        processed_text = preprocessing_text(text)

        # Obtain term doc freq
        term_doc_frequency = self.loaded_dictionary.doc2bow(processed_text)

        # Get the topic distribution for the new document
        topic_distribution = self.loaded_lda_model.get_document_topics(term_doc_frequency)

        # Select the dominant topic (topic with the highest probability)
        dominant_topic = max(topic_distribution, key=lambda x: x[1])

        # Print the dominant topic and its probability
        topic_id, topic_prob = dominant_topic
        # print(f"Dominant Topic: {topic_id}, Probability: {topic_prob}")
        
        return self.id2theme(topic_id)
    
    def id2theme(self, id) -> str:
        """
        ID and theme mapping

        Args:
        - id: predicted id of the theme
            
        Returns: 
        - Theme
        """

        id2theme = {
                0: 'Employee Programs and Support',
                1: 'Medical Treatment and Drug Development',
                2: 'Technology and Software Design',
                3: 'Financial Markets and Trading',
                4: 'Production and Operational Costs',
                5: 'Executive Positions and Leadership',
                6: 'Customer Services and Solutions',
                7: 'Energy and Resource Management',
                8: 'Hospitality and Travel Industry',
                9: 'Transportation and Logistics',
                10: 'Insurance and Risk Management',
                11: 'Property and Investment',
                12: 'Retail Services & Sales',
                13: 'Content and Entertainment Industry',
                14: 'Healthcare Services and Programs',
                15: 'Financial Services and Asset Management',
                16: 'Capital and Financial Regulation',
                17: 'Regulations and Legal Considerations',
                18: 'Product Segmentation and Market',
                19: 'Energy Utility and Customer Service'
            }
        
        return id2theme[id]



