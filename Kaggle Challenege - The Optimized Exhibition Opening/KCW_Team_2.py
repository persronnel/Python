# Ai-My Luong, Ronnel Martinez, Brian Marcelino Owembabazi, Van Hung Le, Rene Adriele Acosta
# Team 2
from collections import defaultdict


class Image:
    def __init__(self, id, type, tags):
        self.id = id
        self.type = type
        self.tags = set(tags)


class Frame:
    def __init__(self, images, tags):
        self.images = images
        self.tags = set(tags)


class ImageOrganizer:
    def __init__(self, images):
        self.images = images
        self.images_by_type = defaultdict(list)
        self.frames = []

        for image in images:
            self.images_by_type[image.type].append(image)

    def create_frames(self):
        landscapes = self.images_by_type.get("L", [])
        portraits = self.images_by_type.get("P", [])

        # Create frames with a landscape image
        for landscape in landscapes:
            frame = Frame([landscape], landscape.tags)
            self.frames.append(frame)

        # Sort portraits by the length of tags
        portraits = sorted(portraits, key=lambda x: len(x.tags))

        for i in range(0, len(portraits), 2):
            if i + 1 < len(portraits):
                portrait_pair = [portraits[i], portraits[i + 1]]
                tags = set.union(portraits[i].tags, portraits[i + 1].tags)
                frame = Frame(list(portrait_pair), tags)
                self.frames.append(frame)
            else:
                portrait_pair = [portraits[i]]
                tags = portraits[i].tags
                frame = Frame(list(portrait_pair), tags)
                self.frames.append(frame)

    def find_next_frame(self, frame, remaining_frames):
        max_common_tags = 0
        next_frame = None

        for candidate_frame in remaining_frames:
            common_tags = len(frame.tags.intersection(candidate_frame.tags))
            if common_tags > max_common_tags:
                max_common_tags = common_tags
                next_frame = candidate_frame
        if next_frame is None:
            next_frame = remaining_frames[0]
        return next_frame

    def create_ordered_list(self):
        remaining_frames = self.frames.copy()
        ordered_frames = []

        # Start with the frame with the most tags
        start_frame = max(remaining_frames, key=lambda f: len(f.tags))
        ordered_frames.append(start_frame)
        remaining_frames.remove(start_frame)

        while remaining_frames:
            last_frame = ordered_frames[-1]
            next_frame = self.find_next_frame(last_frame, remaining_frames)
            if next_frame:
                ordered_frames.append(next_frame)
                remaining_frames.remove(next_frame)
            else:
                break

        return ordered_frames


def find_optimal_order(images):
    organizer = ImageOrganizer(images)
    organizer.create_frames()
    ordered_frames = organizer.create_ordered_list()

    return ordered_frames
