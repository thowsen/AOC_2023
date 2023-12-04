
import { solveDay4 } from "./day4/day4";

const solutions = [
    { solver: solveDay4, day: 4 }
]

const main = () => {

    solutions.forEach((solution) => {
        const { solver, day } = solution;
        const [a, b] = solver();
        console.log(`Day ${day}`)
        console.log(`part A: ${a}`)
        console.log(`part B: ${b}`)
        console.log(`-------------`)
    })


}

main()