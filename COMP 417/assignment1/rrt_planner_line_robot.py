
import random
import drawSample
import sys
import imageToRects
import utils
import numpy as np
import math
import time


def redraw(canvas):
    canvas.clear()
    canvas.markit(tx, ty, r=SMALLSTEP)
    drawGraph(G, canvas)
    for o in obstacles: canvas.showRect(o, outline='blue', fill='blue')
    canvas.delete("debug")


def drawGraph(G, canvas):
    global vertices, nodes, edges
    if not visualize: return
    for i in G[edges]:
        # e.g. vertices: [[10, 270], [10, 280]]
        canvas.polyline([vertices[i[0]], vertices[i[1]]])


# Use this function to generate points randomly for the RRT algo
def genPoint():
    # if args.rrt_sampling_policy == "uniform":
    #     # Uniform distribution
    #     x = random.random()*XMAX
    #     y = random.random()*YMAX
    # elif args.rrt_sampling_policy == "gaussian":
    #     # Gaussian with mean at the goal
    #     x = random.gauss(tx, sigmax_for_randgen)
    #     y = random.gauss(ty, sigmay_for_randgen)
    # else:
    #     print ("Not yet implemented")
    #     quit(1)

    bad = 1
    theta = random.uniform(0, 2 * math.pi)
    while bad:
        bad = 0
        if args.rrt_sampling_policy == "uniform":
            # Uniform distribution
            x = random.random() * XMAX
            y = random.random() * YMAX
        elif args.rrt_sampling_policy == "gaussian":
            # Gaussian with mean at the goal
            x = random.gauss(tx, sigmax_for_randgen)
            y = random.gauss(ty, sigmay_for_randgen)

        else:
            print("Not yet implemented")
            quit(1)
        # range check for gaussian
        if x < 0: bad = 1
        if y < 0: bad = 1
        if x > XMAX: bad = 1
        if y > YMAX: bad = 1
    return [x, y], theta

def compute_endpoint(x, y, theta, length):
    x_end = x + length * math.cos(theta)
    y_end = y + length * math.sin(theta)
    return [x_end, y_end]

def returnParent(k, canvas):
    """ Return parent note for input node k. """
    for e in G[edges]:
        if e[1] == k:
            canvas.polyline([vertices[e[0]], vertices[e[1]]], style=3)
            return e[0]


def genvertex():
    vertices.append(genPoint())
    return len(vertices) - 1


def pointToVertex(p):
    vertices.append(p)
    return len(vertices) - 1


def pickvertex():
    return random.choice(range(len(vertices)))


def lineFromPoints(p1, p2):

    A = p2[1] - p1[1]
    B = p1[0] - p2[0]
    C = A * p1[0] + B * p1[1]
    
    return A, B, C


def pointPointDistance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def closestPointToPoint(G, p2):
    min_distance = float("inf")
    closest_vertex = None
    print(G[nodes])
    for vertex in G[nodes]:       
        distance = pointPointDistance(vertices[vertex], p2)
        if distance < min_distance:
            min_distance = distance
            closest_vertex = vertex
    return closest_vertex




def lineHitsRect(p1, p2, r):
    #Inspired by: https://www.geeksforgeeks.org/line-clipping-set-1-cohen-sutherland-algorithm/
    LEFT, RIGHT, BOTTOM, TOP = 1, 2, 4, 8

    def compute_outcode(x, y, rect):
        outcode = 0
        if x < rect[0]: outcode |= LEFT
        elif x > rect[2]: outcode |= RIGHT
        if y < rect[1]: outcode |= BOTTOM
        elif y > rect[3]: outcode |= TOP
        return outcode

    def segments_intersect(p1, p2, q1, q2):
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

    outcode0 = compute_outcode(p1[0], p1[1], r)
    outcode1 = compute_outcode(p2[0], p2[1], r)

    while True:
        if not (outcode0 | outcode1):  # both endpoints inside rectangle
            # If the endpoints are inside the rectangle, there's no need to further check
            # the Cohen–Sutherland algorithm has done its job.
            return True

        elif outcode0 & outcode1:  # both endpoints outside rectangle, on the same side
            return False

        else:
            x, y = 0.0, 0.0
            # At least one endpoint is outside the clip rectangle; pick it.
            outcode_out = outcode0 if outcode0 else outcode1
            if outcode_out & TOP:
                x = p1[0] + (p2[0] - p1[0]) * (r[3] - p1[1]) / (p2[1] - p1[1])
                y = r[3]
            elif outcode_out & BOTTOM:
                x = p1[0] + (p2[0] - p1[0]) * (r[1] - p1[1]) / (p2[1] - p1[1])
                y = r[1]
            elif outcode_out & RIGHT:
                y = p1[1] + (p2[1] - p1[1]) * (r[2] - p1[0]) / (p2[0] - p1[0])
                x = r[2]
            elif outcode_out & LEFT:
                y = p1[1] + (p2[1] - p1[1]) * (r[0] - p1[0]) / (p2[0] - p1[0])
                x = r[0]

            # Now move outside point to intersection point to clip
            if outcode_out == outcode0:
                p1 = [x, y]
                outcode0 = compute_outcode(x, y, r)
            else:
                p2 = [x, y]
                outcode1 = compute_outcode(x, y, r)

    # Once the Cohen–Sutherland algorithm has trimmed the line segment,
    # Check each edge of the rectangle for an intersection with the line segment
    rect_edges = [
        (r[0], r[1], r[2], r[1]),
        (r[2], r[1], r[2], r[3]),
        (r[0], r[3], r[2], r[3]),
        (r[0], r[1], r[0], r[3])
    ]
    
    for edge in rect_edges:
        q1 = (edge[0], edge[1])
        q2 = (edge[2], edge[3])
        if segments_intersect(p1, p2, q1, q2):
            return True

    return False




def inRect(p, rect, dilation):
    """ Return 1 in p is inside rect, dilated by dilation (for edge cases). """
    x, y = p
    x1, y1, x2, y2 = rect
    if (x1 - dilation <= x <= x2 + dilation) and (y1 - dilation <= y <= y2 + dilation):
        return 1
    else: 
        return 0


def addNewPoint(p1, p2, theta, stepsize):
    distance = pointPointDistance(p1, p2)
    if distance < stepsize:
        return p2, theta
    else:
        theta_direction = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
        return [p1[0] + stepsize * math.cos(theta_direction), p1[1] + stepsize * math.sin(theta_direction)], theta



def rrt_search(G, tx, ty, canvas):
    # Please carefully read the comments to get clues on where to start
    # TODO
    # Fill this function as needed to work ...
    global sigmax_for_randgen, sigmay_for_randgen
     #start_time = time.time()
    n = 0
    nsteps = 0

    iteration_count = 0

    while 1:  # Main loop
        # This generates a point in form of [x,y] from either the normal dist or the Gaussian dist
        p, theta = genPoint()
        iteration_count += 1
        # This function must be defined by you to find the closest point in the existing graph to the guiding point
        cp = closestPointToPoint(G, p)
        v, v_theta = addNewPoint(vertices[cp], p, theta, SMALLSTEP)
        
        if visualize:
            # if nsteps%500 == 0: redraw()  # erase generated points now and then or it gets too cluttered
            n = n + 1
            if n > 10:
                canvas.events()
                n = 0

        robot_start = v
        robot_end = compute_endpoint(v[0], v[1], v_theta, args.robot_length)

        collision_free = True
        for o in obstacles:
            # Check collisions for both start and end positions
            if (lineHitsRect(vertices[cp], robot_start, o) or inRect(robot_start, o, 1)) or \
               (lineHitsRect(vertices[cp], robot_end, o) or inRect(robot_end, o, 1)):
                collision_free = False
                break

        if collision_free:   
            k = pointToVertex(v)  # is the new vertex ID
            orientations.append(v_theta)
            G[nodes].append(k)
            G[edges].append((cp, k))
            if visualize:
                canvas.polyline([vertices[cp], vertices[k]])

            if pointPointDistance(v, [tx, ty]) < SMALLSTEP:
                print("Target achieved.", nsteps, "nodes in entire tree")
                if visualize:
                    t = pointToVertex([tx, ty])  # is the new vertex ID
                    G[edges].append((k, t))
                    if visualize:
                        canvas.polyline([p, vertices[t]], 1)
                    # while 1:
                    #     # backtrace and show the solution ...
                    #     canvas.events()
                    nsteps = 0
                    totaldist = 0
                    while 1:
                        oldp = vertices[k]  # remember point to compute distance
                        k = returnParent(k, canvas)  # follow links back to root.
                        canvas.events()
                        if k <= 1: break  # have we arrived?
                        nsteps = nsteps + 1  # count steps
                        totaldist = totaldist + pointPointDistance(vertices[k], oldp)  # sum lengths

                   # end_time = time.time()
                   # print(end_time - start_time)
                    print("Path length", totaldist, "using", nsteps, "nodes.")
                    print("Iteration Count:", iteration_count, "\n", "Path Length:", nsteps)

                    global prompt_before_next
                    if prompt_before_next:
                        canvas.events()
                        print("More [c,q,g,Y]>")
                        d = sys.stdin.readline().strip().lstrip()
                        print("[" + d + "]")
                        if d == "c": canvas.delete()
                        if d == "q": return
                        if d == "g": prompt_before_next = 0
                    break
                # ... reject
    
    #returning the number of iterations and the path length as a tuple

       


def main():
    # seed
    random.seed(args.seed)
    if visualize:
        canvas = drawSample.SelectRect(xmin=0, ymin=0, xmax=XMAX, ymax=YMAX, nrects=0,
                                       keepcontrol=0)  # , rescale=800/1800.)
        for o in obstacles: canvas.showRect(o, outline='red', fill='blue')
    while 1:
        # graph G
        redraw(canvas)
        G[edges].append((0, 1))
        G[nodes].append(1)
        if visualize: canvas.markit(tx, ty, r=SMALLSTEP)
        drawGraph(G, canvas)
        rrt_search(G, tx, ty, canvas)

    if visualize:
        canvas.mainloop()


if __name__ == '__main__':
    args = utils.get_args()
    visualize = utils.get_args()
    drawInterval = 10  # 10 is good for normal real-time drawing

    prompt_before_next = 1  # ask before re-running sonce solved
    SMALLSTEP = args.step_size  # what our "local planner" can handle.
    map_size, obstacles = imageToRects.imageToRects(args.world)
    # Note the obstacles are the two corner points of a rectangle (left-top, right-bottom)
    # Each obstacle is (x1,y1), (x2,y2), making for 4 points

    XMAX = map_size[0]
    YMAX = map_size[1]
    # The boundaries of the world are (0,0) and (XMAX,YMAX)

    G = [[0], []]  # nodes, edges
    # vertices = [[args.start_pos_x, args.start_pos_y], [args.start_pos_x, args.start_pos_y + 10]]
    vertices = [(args.start_pos_x, args.start_pos_y), (args.start_pos_x, args.start_pos_y + 10)]
    orientations = [0]

    # goal/target
    tx = args.target_pos_x
    ty = args.target_pos_y

    # start
    sigmax_for_randgen = XMAX / 2.0
    sigmay_for_randgen = YMAX / 2.0
    nodes = 0
    edges = 1

    main()
