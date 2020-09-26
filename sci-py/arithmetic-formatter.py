def transpose_matrix(matrix):
    result = []
    for i in range(len(matrix[0])):
        result.append([row[i] for row in matrix])
    return result


def arrange_problem(problem, show_result=False):
    first, operator, second = problem.split()

    if operator not in "+-":
        raise ValueError("Error: Operator must be '+' or '-'.")
    if not first.isdigit() or not second.isdigit():
        raise ValueError("Error: Numbers must only contain digits.")
    if len(first) > 4 or len(second) > 4:
        raise ValueError("Error: Numbers cannot be more than four digits.")

    width = max(len(first), len(second))
    lines = [
        f"  {first:>{width}}",
        f"{operator} {second:>{width}}",
        "-" * (width + 2),
    ]

    if show_result:
        if operator == "+":
            result = int(first) + int(second)
        elif operator == "-":
            result = int(first) - int(second)
        lines.append(f"{result:>{width+2}}")

    return lines


def arithmetic_arranger(problems, show_result=False):
    if len(problems) > 5:
        return "Error: Too many problems."

    try:
        lines = transpose_matrix([arrange_problem(problem, show_result) for problem in problems])
    except ValueError as e:
        return str(e)

    return "\n".join("    ".join(segment for segment in line) for line in lines)
