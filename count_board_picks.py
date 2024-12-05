def count_board_pick_coordinates(filename):
    file = open(filename)
    # A1, H1, A8, H8
    pose_lines = []
    poses = []
    for line in file:
        pose_lines.append(line[0:-1].split(","))

    j = 0
    k = 0
    poses.append([])
    for i in range(0, len(pose_lines)):
        if i == 4:
            k = 1
            j = 0
            poses.append([])
        if i % 2 == 0:
            # poses.append([])
            poses[k].append([])
            poses[k][j].append(float(pose_lines[i][0][4:]))
            poses[k][j].append(float(pose_lines[i][1][5:]))
            poses[k][j].append(float(pose_lines[i][2][5:]))
        else:
            poses[k][j].append(float(pose_lines[i][0][7:]))
            poses[k][j].append(float(pose_lines[i][1][9:]))
            poses[k][j].append(float(pose_lines[i][2][7:]))
            j += 1

    # print(poses)

    poses[0][0][2] += 0.01
    poses[0][1][2] += 0.01
    poses[1][0][2] += 0.01
    poses[1][1][2] += 0.01

    # count coordinates for 1 and 8 row
    for j in range(0, 2):
        for i in range(0, 6):
            poses[j].insert(1, [])
        for i in range(0, 6):
            dp = (poses[j][0][i] - poses[j][7][i]) / 7
            for k in range(1, 7):
                poses[j][k].append(round(poses[j][0][i] - k * dp, 4))
        # test for roll
        # for i in range(1, 7):
        #     poses[j][i][3] = poses[j][0][3]
    for i in range(1, 7):
        poses.insert(1, [[],[],[],[],[],[],[],[]])

    for column in range(0, 8):
        for parameter in range(0,6):
            dp = (poses[7][column][parameter] - poses[0][column][parameter]) / 7
            for row in range(1, 7):
                poses[row][column].append(round(poses[0][column][parameter] + row * dp, 4))

    for l in poses:
        for k in l:
            print(k[3], end = '\t')
        print()
    return poses

count_board_pick_coordinates("board_poses4.txt")
