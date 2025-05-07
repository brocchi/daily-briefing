import os
import unittest
from unittest.mock import patch, mock_open
from utils.keywords import load_required_keywords, check_content_has_keywords


class TestLoadRequiredKeywords(unittest.TestCase):

    @patch('os.path.exists')
    def test_keywords_file_does_not_exist(self, mock_exists):
        # Simula que o arquivo não existe
        mock_exists.return_value = False
        result = load_required_keywords()
        self.assertEqual(result, [])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="# Comment line\n\nkeyword1\nkeyword2\n")
    def test_keywords_file_with_valid_data(self, mock_open, mock_exists):
        # Simula que o arquivo existe
        mock_exists.return_value = True
        result = load_required_keywords()
        self.assertEqual(result, ['keyword1', 'keyword2'])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="# Comment line\n\nKEYWORD1\nKEYWORD2\n")
    def test_keywords_file_case_insensitive(self, mock_open, mock_exists):
        # Simula que o arquivo existe e verifica se as palavras são convertidas para lowercase
        mock_exists.return_value = True
        result = load_required_keywords()
        self.assertEqual(result, ['keyword1', 'keyword2'])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="# Comment line\n\n\n")
    def test_keywords_file_with_only_comments_and_empty_lines(self, mock_open, mock_exists):
        # Simula que o arquivo existe, mas contém apenas comentários e linhas vazias
        mock_exists.return_value = True
        result = load_required_keywords()
        self.assertEqual(result, [])


class TestCheckContentHasKeywords(unittest.TestCase):

    @patch('utils.keywords.load_required_keywords')
    def test_no_required_keywords(self, mock_load_keywords):
        # Simula que não há palavras-chave carregadas
        mock_load_keywords.return_value = []
        content = "This is a test content."
        result = check_content_has_keywords(content)
        self.assertEqual(result, (True, []))

    def test_content_contains_required_keywords(self):
        # Testa quando o conteúdo contém palavras-chave
        content = "This is a test content with keyword1."
        required_words = ["keyword1", "keyword2"]
        result = check_content_has_keywords(content, required_words)
        self.assertEqual(result, (True, required_words))

    def test_content_does_not_contain_required_keywords(self):
        # Testa quando o conteúdo não contém palavras-chave
        content = "This is a test content without any keywords."
        required_words = ["keyword1", "keyword2"]
        result = check_content_has_keywords(content, required_words)
        self.assertEqual(result, (False, required_words))

    def test_case_insensitivity(self):
        # Testa se a busca é case-insensitive
        content = "This is a Test Content with KEYWORD1."
        required_words = ["keyword1", "keyword2"]
        result = check_content_has_keywords(content, required_words)
        self.assertEqual(result, (True, required_words))

    def test_partial_word_match(self):
        # Testa se a busca não considera partes de palavras
        content = "This is a test content with keyword123."
        required_words = ["keyword1", "keyword2"]
        result = check_content_has_keywords(content, required_words)
        self.assertEqual(result, (False, required_words))


if __name__ == '__main__':
    unittest.main()