# Ai-My Luong, Ronnel Martinez, Brian Marcelino Owembabazi, Van Hung Le, Rene Adriele Acosta
# Team 2
from KCW_Team_2 import *
import time

class Scorer():

    def __init__(self,input_file,sub_file):

        self.frameglasses = {}
        self.usedframeglasses = {}
        self.sub = open(sub_file,"r")
        self.actual_frameglass = []
        self.prev_frameglass = []
        self.score = 0
        self.debug = False

        f = open(input_file, "r")
        for count, i in enumerate(f.readlines()[1:]):
            self.frameglasses[count] = i.split()
            self.usedframeglasses[count] = False

    def frameglass_checking(self,frameglass_elements):

        if len(frameglass_elements) == 1:
            if self.frameglasses[int(frameglass_elements[0])][0] == "L":
                if (self.usedframeglasses[int(frameglass_elements[0])] == True):
                    raise Exception('Error:', 'Multiple use of frameglasses ' + frameglass_elements[0])
                tags = self.frameglasses[int(frameglass_elements[0])][2:]
                self.usedframeglasses[int(frameglass_elements[0])] = True
                return tags
            else:
                raise Exception('Error:', 'THE TYPE OF PAINTING')
        elif len(frameglass_elements) == 2:
            if self.frameglasses[int(frameglass_elements[0])][0] == "P" and self.frameglasses[int(frameglass_elements[1])][0] == "P":
                if self.usedframeglasses[int(frameglass_elements[0])] == True:
                    raise Exception('Error:', 'Multiple use of frameglasses ' + frameglass_elements[0])
                if self.usedframeglasses[int(frameglass_elements[1])] == True:
                    raise Exception('Error:', 'Multiple use of frameglasses ' + frameglass_elements[1])
                tags = list(set(self.frameglasses[int(frameglass_elements[0])][2:]+self.frameglasses[int(frameglass_elements[1])][2:]))
                self.usedframeglasses[int(frameglass_elements[0])] = True
                self.usedframeglasses[int(frameglass_elements[1])] = True
                return tags
            else:
                raise Exception('Error:', 'THE TYPE OF PAINTING')
        else:
            raise Exception('Error:', 'THE TYPE OF PAINTING')

    def exhibition_walk(self):

        for frame in self.sub.readlines()[1:]:

            self.actual_frameglass = self.frameglass_checking(frame.strip().split())
            if self.prev_frameglass != []:
                self.scorer(self.actual_frameglass, self.prev_frameglass)
            self.prev_frameglass = self.actual_frameglass

    def scorer(self,frame1,frame2):

        intersection = list(set(frame1).intersection(frame2))
        val1 = len(intersection)
        val2 = len(frame1)-len(intersection)
        val3 = len(frame2)-len(intersection)
        self.score += min(val1,val2,val3)

def write_result(file_path, ordered_frames):
    # Write output to a file
    output_file_path = ("output_" + file_path)
    # Replace with the desired output file path
    with open(output_file_path, "w") as output_file:
        output_file.write(f"{len(ordered_frames)}\n")
        for frame in ordered_frames:
            if len(frame.images) == 1:
                output_file.write(f"{frame.images[0].id}\n")
            else:
                output_file.write(f"{frame.images[0].id} {frame.images[1].id}\n")
    return output_file_path


def organize_paintings(file_path):
    with open(file_path, "r") as file:
        # Read the number of paintings
        num_paintings = int(file.readline().strip())
        # Read and parse each painting
        images = []
        for _ in range(num_paintings):
            painting_type, num_tags, *tags = file.readline().strip().split()
            painting_id = len(images)
            img = Image(painting_id, painting_type, tags)
            images.append(img)

        # sort images
        sorted_images = sorted(images, key=lambda x: len(x.tags))
        if file_path == '11_randomizing_paintings.txt':
            MAX_NUMBER_IMAGES = 1000
        else:
            MAX_NUMBER_IMAGES = 20000
        # Split the sorted_images list into chunks of size MAX_NUMBER_IMAGES
        image_chunks = [
            sorted_images[i : i + MAX_NUMBER_IMAGES]
            for i in range(0, len(sorted_images), MAX_NUMBER_IMAGES)
        ]
        # verify even number of portrait images in each chunk
        for i in range(len(image_chunks)):
            chunk = image_chunks[i]
            portrait_images = [img for img in chunk if img.type == "P"]
            if len(portrait_images) % 2 == 1:
                if i + 1 < len(image_chunks):
                    last_img = portrait_images[-1]
                    image_chunks[i + 1].append(last_img)
                    image_chunks[i].remove(last_img)

        final_frames = []
        for i in range(len(image_chunks)):
            images = image_chunks[i]
            # Create image organizer
            organizer = ImageOrganizer(images)
            organizer.create_frames()
            ordered_frames = organizer.create_ordered_list()
            final_frames += ordered_frames

        # write output result
        output_file_path = write_result(file_path, final_frames)
        # print score
        score = Scorer(file_path, output_file_path)
        score.exhibition_walk()
        return score.score

def main():
    files = ['0_example.txt','10_computable_moments.txt','110_oily_portraits.txt','11_randomizing_paintings.txt','1_binary_landscapes.txt']
    final_score = 0
    start_time = time.time()
    for input_file_path in files:
        score = organize_paintings(input_file_path)
        print(f'input file: {input_file_path} ---> score: {score}' )
        final_score += score
    time_exec = round((time.time() - start_time)/60, 2)
    print(f"Total time execution : {time_exec} min")
    print(f"Final score of 5 input files : {final_score}")

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(err)          # __str__ allows args to be printed directly,