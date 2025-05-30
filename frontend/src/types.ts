export interface QueryResult {
    [key: string]: string | number | null;
}

export type Answer = {
    sql: string,
    data: QueryResult[]
}

export enum Vote {
    UP,
    DOWN
}