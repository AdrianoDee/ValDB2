export type ReportEditorMode = 'edit' | 'view' | 'readonly'

export interface Response <T> {
    status: 'ok' | 'error'
    message?: string
    data?: T
} 

export interface Category {
    name: string
    subcategories: {
        name: string
        groups: string[]
    }[]
}

export interface Report {
    id: string
    name: string
}

export interface User {
    name: string
}

export interface Activity {
    content: string
}

export interface CampaignReportGroup {
    name: string
    report?: Report
}

export interface CampaignGroup {
    category: string
    subcategories: {
        subcategory: string
        groups: CampaignReportGroup[]
    }[]
}

export enum ReportStatus {
    OK = 1,
    NOT_YET_DONE = 2,
    FAILURE = 3,
    CHANGES_EXPECTED = 4,
    IN_PROGRESS = 5,
    KNOWN_ISSUE = 6,
}

export interface Report {
    id: string
    authors: User[]
    group: string
    campaign_name: string
    status: ReportStatus
    content: string
    activity: Activity[]
}

export interface Campaign {
    id: string
    name: string
    description: string
    manager: User
    deadline: string // 2020-21-2
    target_release: string
    reference_release: string
    subcategories: string[]
    report: Report[]
    active: boolean
    created_at: string // 2020-21-2
    updated_at: string // 2020-21-2
}