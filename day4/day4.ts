import { readFileSync } from "fs"
import _ from 'lodash';


const clean = (line: string): number[] => {
    return line
        .trim()
        .split(' ')
        .reduce((acc: number[], e: string) => {
            const num = parseInt(e.trim())
            return !!num ? [...acc, num] : acc
        }, [])
}


const solveA = (lines: string[]): number => {
    const winning = /:((\s+\d+)+)\s\|/g
    const drawn = /((\s+(\d+))+)$/g
    return lines.reduce((acc, line) => {
        winning.lastIndex = 0
        drawn.lastIndex = 0

        const matches_winning_raw = winning.exec(line)
        const matched_drawn_raw = drawn.exec(line)

        if (!Array.isArray(matches_winning_raw) ||
            !Array.isArray(matched_drawn_raw)) return acc

        const matches_winning = clean(matches_winning_raw[1])
        const matches_drawn = clean(matched_drawn_raw[1]);

        const score = Math.floor(
            2 ** (matches_drawn.filter(e => matches_winning.includes(e)).length - 1))

        return acc + score
    }, 0)


}


type ProcessedLotteryTicket = { id: number, copiesGenerated: number[] }


const processLotteryTicket = (id: number, line: string): ProcessedLotteryTicket => {
    const winning_regex = /:((\s+\d+)+)\s\|/g
    const drawn_regex = /((\s+(\d+))+)$/g

    const winning_raw = winning_regex.exec(line);
    const drawn_raw = drawn_regex.exec(line)
    if (winning_raw === null || drawn_raw === null) throw `failed to extract id for row: ${line}`

    const winning_numbers = clean(winning_raw[1])
    const drawn_numbers = clean(drawn_raw[1])

    const copiesGenerated = drawn_numbers.filter(e => winning_numbers.includes(e))
    return { id, copiesGenerated: _.range(id + 1, (id + 1) + copiesGenerated.length) }

}


const solveB = (lines: string[]): number => {
    const mem_map = new Map<number, ProcessedLotteryTicket>()
    const work_stack: ProcessedLotteryTicket[] = []
    let scratchedTickets: number = 0;

    lines.forEach((e) => {
        const id_regex = /^Card\s+(\d+).*$/
        const id_raw = id_regex.exec(e);
        if (id_raw === null) throw `failed to extract id for row: ${e}`
        const id = parseInt(id_raw[1].trim())
        const lotteryTicket = processLotteryTicket(id, e)
        mem_map.set(id, lotteryTicket)
        work_stack.push(lotteryTicket)
    })

    while (work_stack.length > 0) {
        const curr_ticket = work_stack.pop()
        if (curr_ticket === undefined) throw 'this should not happen 1'
        scratchedTickets++;
        curr_ticket.copiesGenerated.forEach((e) => {
            const work = mem_map.get(e)
            if (work === undefined) throw 'this should not happen 2'
            work_stack.push(work);
        })
    }
    return scratchedTickets
}


export const solveDay4 = () => {
    const lines = readFileSync('day4/input.csv', 'utf-8')
        .trim()
        .split('\n')
        .map(e => e.trim())

    const a = solveA(lines)
    const b = solveB(lines)
    return [a, b]
}