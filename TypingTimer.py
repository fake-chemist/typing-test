import pygame
from pygame.locals import *
import sys
import time
import random
from random_word import RandomWords


class TypingTest:

    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Typing Timer Test")
        
        self.font = pygame.font.Font(None, 48)
        self.clock = pygame.time.Clock()
        self.difficulty_rating = random.randint(28, 184)
        self.user_typed_words = []
        self.testing_words = ['Geeks', 'For', 'Geeks']
        self.testing_word_ending = []
        self.current_word = ""
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.time_limit = 60  # 1-minute timer
        self.time_remaining = self.time_limit
        self.running = True
        self.score = 0


    def random_strings(self):
        #create list of random words
        r = RandomWords()
        self.testing_words = [r.get_random_word() for _ in range(self.difficulty_rating)]
    
    def word_picker(self):
        #get word from word list
        if self.testing_words:
            self.current_word = self.testing_words.pop(0)
            self.testing_word_ending.append(self.current_word)
        else:
            raise ValueError("All words typed")

    def calculate_accuracy(self):
        first_list = self.testing_word_ending
        second_list = self.user_typed_words

        if not first_list:  # Avoid division by zero
            return 0.0

        count = 0
        # Compare each element in the same order, up to the length of the user-typed list
        for expected, actual in zip(first_list, second_list):
            if expected == actual:
                count += 1

        # Compute the similarity percentage based on the length of the original list
        similarity_percentage = (count / len(first_list)) * 100

        return similarity_percentage
    
    def reset_game(self):
        #reset things for next game
        self.user_input = ""
        self.start_time = time.time()
        self.end_time = None
        self.time_remaining = self.time_limit
        self.score = 0
        self.random_strings()
        self.user_typed_words = []
        self.word_picker() 

    def display_results(self):
        if self.end_time is None: 
            time_taken = 60
        else:
            time_taken = self.end_time - self.start_time

        accuracy = self.calculate_accuracy()
        
        result_text = f"Time: {time_taken:.2f}s |WPM: {len(self.user_typed_words)} |Accuracy: {accuracy:.2f}% "
        result_surface = self.font.render(result_text, True, (255, 255, 255))
        self.screen.blit(result_surface, (50, 300))

    def run(self):
        self.reset_game()
        while self.running:
            self.screen.fill((0, 0, 0))

            # Update timer
            elapsed_time = time.time() - self.start_time
            self.time_remaining = max(0, self.time_limit - elapsed_time)

            # Display current word
            word_surface = self.font.render(self.current_word, True, (255, 255, 255))
            self.screen.blit(word_surface, (50, 100))

            # Display user input
            input_surface = self.font.render(self.user_input, True, (0, 255, 0))
            self.screen.blit(input_surface, (50, 200))

            # Display timer
            timer_surface = self.font.render(f"Time Left: {int(self.time_remaining)}s", True, (255, 255, 255))
            self.screen.blit(timer_surface, (50, 50))

            # Check if time is up
            if (self.time_remaining <= 0) or (self.end_time is not None):
                self.display_results()
                pygame.display.flip()
                pygame.time.wait(5000)  # Wait for 5 seconds before exiting
                self.running = False
                continue
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if self.user_input:
                            self.user_typed_words.append(self.user_input)
                            try: 
                                self.word_picker()
                            except ValueError:
                                self.end_time = time.time()
                        self.user_input = ""  # Clear input after submission
                    elif event.key == K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += event.unicode

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    TypingTest().run()
    pygame.quit()
    sys.exit()

