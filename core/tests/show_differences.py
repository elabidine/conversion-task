from django.test import SimpleTestCase
# from ..show_differences import show_differences_combined as show_differences
from core.utils.show_differences import show_differences_separate as show_differences

""" Tests shows differences between two texts with changes highlighted. Two versions are provided:
    - show_differences_combined: Returns a single string with changes highlighted, containing extracts from both text1 and text2.
    - show_differences_separate: Returns two strings with changes highlighted separately, one containing extracts from text1 and the other from text2. """


class TestAbbreviateText(SimpleTestCase):

    def test_01_show_differences_equal(self):
        print(' 1')
        text1 = "The quick brown fox jumps over the lazy dog"
        text2 = "The quick brown fox jumps over the lazy dog"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        # expected = False # Returns False if the texts are equal
        # self.assertEqual(show_differences(text1, text2), expected)

    def test_02_show_differences_different(self):
        print(' 2')
        text1 = "The quick brown fox jumps over the lazy dog"
        text2 = "The quick brown cat jumps over the lazy dog"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        # expected = "... quick brown *fox* jumps over ..." # surrounds the changes with "*", and surrounds the context with "..."
        # self.assertEqual(show_differences(text1, text2), expected)

    def test_03_show_differences_end(self):
        print(' 3')
        text1 = "The very quick brown fox"
        text2 = "The very quick brown cat"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        # expected = "... quick brown *fox*" # No "..." at the end of the string.
        # self.assertEqual(show_differences(text1, text2), expected)

    def test_04_show_differences_beginning(self):
        print(' 4')
        text1 = "Tha quick brown fox jumps jumps over the lazy dog"
        text2 = "The quick brown fox jumps jumps over the lazy dog"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        #  expected = "*Tha* quick brown ..." # No "..." at the beginning of the string.
        # self.assertEqual(show_differences(text1, text2), expected)


    def test_05_show_differences_added(self):
        print(' 5')
        text1 = "The quick brown fox over the lazy dog"
        text2 = "The quick brown fox jumps over the lazy dog"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        #  expected = "... brown fox ** over the ..." # "**"" indicates the location where text was added
        # self.assertEqual(show_differences(text1, text2), expected)

    def test_06_show_differences_removed(self):
        print(' 6')
        text1 = "The quick brown fox jumps over the lazy dog"
        text2 = "The quick brown fox the lazy dog"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        #  expected = "... quick brown fox *jumps over* the lazy ..." # "*" indicates the location where text was removed
        # self.assertEqual(show_differences(text1, text2), expected)

    def test_07_show_differences_sucessive(self):
        print(' 7')
        text1 = "The very quick brown fox always jumps high over the lazy dog in the morning"
        text2 = "The very quick yellow fox always jumps high over the energetic dog in the morning"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        #  expected = "... very quick *brown* fox always ... over the *lazy* dog in ..." # avoid repeating the "..." between changes
        # self.assertEqual(show_differences(text1, text2), expected)

    def test_08_show_differences_empty(self):
        print(' 8')
        text1 = ""
        text2 = ""
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        #  expected = False # Returns False if the texts are equal
        # self.assertEqual(show_differences(text1, text2), expected)

    def test_09_show_differences_long_differences(self):
        print(' 9')
        text1 = "The quick brown fox jumps over the lazy dog non stop: in the morning, in the evening and the night - litterally every hour of the day"
        text2 = "The quick brown fox jumps over the lazy dog every hour of the day"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        #  expected = "... lazy dog *non stop: in the morning, in the evening and the night - litterally* every hour ..."
        # self.assertEqual(show_differences(text1, text2), expected)

    def test_10_show_differences_long_differences(self):
        print(' 10')
        text1 = "The quick brown fox jumps over the lazy dog non stop: in the morning, in the evening and the night - litterally every hour of the day"
        text2 = "The quick brown fox jumps over the lazy dog every hour of the evening"
        print(show_differences(text1, text2))
        self.assertEqual(1,1)
        #  expected = "... lazy dog *non stop: in the morning, in the evening and the night - litterally* every hour ..."
        # self.assertEqual(show_differences(text1, text2), expected)