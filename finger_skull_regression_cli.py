import math
import re


def parse_numbers(s: str):
    nums = re.findall(r"-?\d+(?:\.\d+)?", s)
    return [float(x) for x in nums]


def t_critical_approx(confidence: float, df: int) -> float:
    # Two-tailed t*: quantile(1 - alpha/2). Uses a normal-based series expansion.
    z_map = {0.90: 1.6448536269514722, 0.95: 1.959963984540054, 0.99: 2.5758293035489004}
    z = z_map.get(round(confidence, 2), 1.959963984540054)
    if df <= 0:
        return float("nan")

    z2 = z * z
    z3 = z2 * z
    z5 = z3 * z2
    z7 = z5 * z2

    df1 = float(df)
    return (
        z
        + (z3 + z) / (4 * df1)
        + (5 * z5 + 16 * z3 + 3 * z) / (96 * df1 * df1)
        + (3 * z7 + 19 * z5 + 17 * z3 - 15 * z) / (384 * df1 * df1 * df1)
    )


def compute(finger_values, skull_values, prediction_at, confidence=0.95):
    n = min(len(finger_values), len(skull_values))
    if n < 3:
        raise ValueError("Need at least 3 (x,y) pairs")
    if len(finger_values) != len(skull_values):
        raise ValueError(f"Counts differ: finger={len(finger_values)}, skull={len(skull_values)}")

    finger_sum = sum(finger_values)
    skull_sum = sum(skull_values)
    finger_sum_sq = sum(x * x for x in finger_values)
    skull_sum_sq = sum(y * y for y in skull_values)
    finger_skull_sum = sum(x * y for x, y in zip(finger_values, skull_values))

    Sxx = finger_sum_sq - (finger_sum * finger_sum) / n
    Syy = skull_sum_sq - (skull_sum * skull_sum) / n
    Sxy = finger_skull_sum - (finger_sum * skull_sum) / n

    if Sxx == 0:
        raise ValueError("Sxx is 0 (all X values identical). Cannot fit regression.")

    B1 = Sxy / Sxx
    B0 = (skull_sum - B1 * finger_sum) / n

    SSE = Syy - B1 * Sxy
    df = n - 2
    error_var = SSE / df

    SE_B1 = math.sqrt(error_var / Sxx)
    xbar = finger_sum / n
    SE_B0 = math.sqrt(error_var * (1 / n + (xbar * xbar) / Sxx))

    SE_at_prediction = math.sqrt(error_var * (1 / n + (prediction_at - xbar) ** 2 / Sxx))

    tcrit = t_critical_approx(confidence, df)

    yhat = B0 + B1 * prediction_at
    CI_of_prediction = (yhat - tcrit * SE_at_prediction, yhat + tcrit * SE_at_prediction)

    t_statistic = B1 / SE_B1
    CI_of_slope = (B1 - tcrit * SE_B1, B1 + tcrit * SE_B1)
    R_squared = float("nan") if Syy == 0 else 1 - (SSE / Syy)

    return {
        "n": n,
        "df": df,
        "tcrit": tcrit,
        "finger_sum": finger_sum,
        "skull_sum": skull_sum,
        "finger_sum_sq": finger_sum_sq,
        "skull_sum_sq": skull_sum_sq,
        "finger_skull_sum": finger_skull_sum,
        "Sxx": Sxx,
        "Syy": Syy,
        "Sxy": Sxy,
        "B1": B1,
        "B0": B0,
        "SSE": SSE,
        "error_var": error_var,
        "SE_B1": SE_B1,
        "SE_B0": SE_B0,
        "prediction_at": prediction_at,
        "yhat": yhat,
        "SE_at_prediction": SE_at_prediction,
        "CI_of_prediction": CI_of_prediction,
        "t_statistic": t_statistic,
        "CI_of_slope": CI_of_slope,
        "R_squared": R_squared,
    }


def fx(v):
    return f"{v:.6f}" if isinstance(v, (float, int)) and math.isfinite(v) else str(v)


def main():
    print("Enter finger (X) values (comma/space/newline separated). End input with an empty line:")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    finger = parse_numbers("\n".join(lines))

    print("\nEnter skull (Y) values (comma/space/newline separated). End input with an empty line:")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    skull = parse_numbers("\n".join(lines))

    prediction_at = float(input("\nPredict at X = ").strip())
    confidence = float(input("Confidence (0.90/0.95/0.99) [0.95]: ").strip() or "0.95")

    r = compute(finger, skull, prediction_at, confidence)

    while True:
        print(
            "\nMENU\n"
            "1) Data summary\n"
            "2) Totals & cross-products\n"
            "3) Sxx, Syy, Sxy\n"
            "4) Fitted model + errors\n"
            "5) Prediction + CI\n"
            "6) Slope test + R^2\n"
            "9) Show ALL\n"
            "0) Exit"
        )
        choice = input("Choose: ").strip()

        def show_summary():
            print(f"n={r['n']}, df={r['df']}, t*≈{fx(r['tcrit'])}")

        def show_totals():
            print(
                f"Σx={fx(r['finger_sum'])}\nΣy={fx(r['skull_sum'])}\n"
                f"Σx^2={fx(r['finger_sum_sq'])}\nΣy^2={fx(r['skull_sum_sq'])}\nΣxy={fx(r['finger_skull_sum'])}"
            )

        def show_s():
            print(f"Sxx={fx(r['Sxx'])}\nSyy={fx(r['Syy'])}\nSxy={fx(r['Sxy'])}")

        def show_model():
            print(
                f"B1={fx(r['B1'])}\nB0={fx(r['B0'])}\n"
                f"Model: Y = {fx(r['B0'])} + {fx(r['B1'])} X\n\n"
                f"SSE={fx(r['SSE'])}\nError variance={fx(r['error_var'])}\n"
                f"SE(B1)={fx(r['SE_B1'])}\nSE(B0)={fx(r['SE_B0'])}"
            )

        def show_prediction():
            lo, hi = r["CI_of_prediction"]
            print(
                f"Predicted Y at X={r['prediction_at']}: {fx(r['yhat'])}\n"
                f"SE at prediction: {fx(r['SE_at_prediction'])}\n"
                f"CI: ({fx(lo)}, {fx(hi)})"
            )

        def show_inference():
            lo, hi = r["CI_of_slope"]
            significant = abs(r["t_statistic"]) > r["tcrit"]
            print(
                f"t-statistic={fx(r['t_statistic'])}\n"
                f"Significant slope? {'YES' if significant else 'NO'}\n"
                f"CI(slope)=({fx(lo)}, {fx(hi)})\n"
                f"R^2={fx(r['R_squared'])}"
            )

        if choice == "1":
            show_summary()
        elif choice == "2":
            show_totals()
        elif choice == "3":
            show_s()
        elif choice == "4":
            show_model()
        elif choice == "5":
            show_prediction()
        elif choice == "6":
            show_inference()
        elif choice == "9":
            show_summary()
            show_totals()
            show_s()
            show_model()
            show_prediction()
            show_inference()
        elif choice == "0":
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
