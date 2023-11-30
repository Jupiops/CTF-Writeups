from queue import PriorityQueue

import cv2
import numpy as np
from PIL import Image


# Define the heuristic function for A* search
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(image, start, goal):
    """
    Perform A* search to find the path from start to goal in the maze, while staying on the colorful path.
    """
    # Priority queue to store the nodes to explore, sorted by priority
    frontier = PriorityQueue()
    frontier.put((0, start))

    # Dictionaries to store the cost to reach each node and the path to each node
    cost_so_far = {start: 0}
    came_from = {start: None}

    # Directions to move in the maze
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Loop until there are no more nodes to explore or the goal is found
    while not frontier.empty():
        _, current = frontier.get()

        # Check if the goal has been reached
        if current == goal:
            break

        # Explore neighboring nodes
        for direction in directions:
            next_node = (current[0] + direction[0], current[1] + direction[1])

            # Check if the next node is within the image boundaries
            if 0 <= next_node[0] < image.shape[0] and 0 <= next_node[1] < image.shape[1]:
                # Get the color of the next node
                color = image[next_node]

                # Assign a high cost to white and black pixels, and a low cost to colorful pixels
                if (color == [255, 255, 255]).all() or (color == [0, 0, 0]).all():
                    cost = 100_000_000  # High cost for white and black
                else:
                    cost = 1  # Low cost for colorful pixels

                new_cost = cost_so_far[current] + cost

                # If the next node hasn't been visited or a cheaper path has been found, update the data structures
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    frontier.put((priority, next_node))
                    came_from[next_node] = current

    # Reconstruct the path from the start to the goal
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path


def highlight_path(image, path, output_image_path):
    # Highlight the path
    path_color = [0, 0, 255]  # BGR format
    for point in path:
        color = image[tuple(point)]
        if (color == [0, 0, 0]).all() or (color == [255, 255, 255]).all():
            # If the path is crossing a black or white tile, shift the color
            path_color = path_color[1:] + path_color[: 1]
            print("The path is crossing a black or white tile!")
        image[tuple(point)] = path_color

    # Save the new image
    cv2.imwrite(output_image_path, image)

    print(f"The path has been highlighted and saved to {output_image_path}")


def collect_colors_along_path(image, path):
    """
    Collect the colors along the given path in the image.
    """
    colors = []
    for point in path:
        colors.append(image[tuple(point)].tolist())
    return colors


def rgb2hex(val):
    r = hex(val[0])[2:].zfill(2)
    g = hex(val[1])[2:].zfill(2)
    b = hex(val[2])[2:].zfill(2)
    return bytes.fromhex((r + g + b))


if __name__ == '__main__':
    maze_num = 1
    while True:
        # Load the image
        image_path = f'maze_{maze_num}.png'

        image = Image.open(image_path)

        # Convert the image to a numpy array
        image_np = np.array(image)

        # Define the start and end points of the maze
        start = (0, 2)
        goal = (image_np.shape[0] - 1, image_np.shape[1] - 3)
        print(f'Start tile color: {start}, Goal tile color: {goal}')

        # Find the path from start to goal
        path = a_star_search(image_np, start, goal)

        # Display the first 10 points in the path as a sample
        print(path[:10])
        # with open(f'path_maze_{maze_num}.json', 'w') as f:
        #     f.write(json.dumps(path))

        # Load the path array from the JSON file
        # with open(f'path_maze_{maze_num}.json', 'r') as f:
        #     path = json.load(f)

        # Highlight the path in the image and save the new image
        highlight_path(np.copy(image_np), path, f'maze_{maze_num}_solved.png')

        # Collect the colors along the path
        colors_along_path = collect_colors_along_path(image_np, path)
        # with open('colors_along_path_maze_2.json', 'r') as f:
        #     colors_along_path = json.load(f)

        # Display the first 10 colors along the path as a sample
        print(len(colors_along_path))
        print(colors_along_path[:10])
        print([rgb2hex(x) for x in colors_along_path[:10]])

        # with open(f'colors_along_path_maze_{maze_num}.json', 'w') as f:
        #     f.write(json.dumps(colors_along_path))
        maze_num += 1

        # convert each pixels RGB values to hex
        data = b''.join([rgb2hex(x) for x in colors_along_path])
        # write each byte of hex data into a file called decoded.png
        with open(f'maze_{maze_num}.png', 'wb') as f:
            f.write(data)

        if b'\x89PN' not in data:
            print("Not a PNG")
            break
