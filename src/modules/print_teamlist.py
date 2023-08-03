def print_teamlist(df, decisions, captain_decisions, sub_decisions, inputs):
    expected_scores, prices, position, team, names = inputs
    pos_map = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
    with open("../output/teamlist.txt", "w") as f:
        f.write("Starting 11: \n")
        predict_total = 0
        real_total = 0

        for i in range(len(decisions)):
            if decisions[i].value() != 0:
                f.write(
                    f"{names[i]} {pos_map[position[i]]}: {round(float(expected_scores[i]), 2)} points predicted at $ {prices[i]} "
                )
                if captain_decisions[i].value() == 1:
                    f.write("TEAM CAPTAIN")
                    real_total += 2 * df[df.Player == names[i]].FPL_points.values[0]
                    predict_total += 2 * expected_scores[i]

                f.write("\n")
                real_total += df[df.Player == names[i]].FPL_points.values[0]
                predict_total += expected_scores[i]

        f.write("\n \nSubs:\n")

        for j in range(len(sub_decisions)):
            if sub_decisions[j].value() != 0:
                f.write(
                    f"{names[j]} {pos_map[position[j]]}: {round(float(expected_scores[j]), 2)} points at ${prices[j]} \n"
                )

        f.write(f"\n \nPredicted Point Total: {round(predict_total, 2)} \n")
        f.write(f"Real Point Total: {real_total} \n")
