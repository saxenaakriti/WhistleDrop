export const openApiSpec = {
    openapi: "3.0.2",
    info: {
        title: "WhistleDrop",
        description: "WhistleDrop — Speak Without Being Seen. A confidential reporting backend system allowing individuals to submit anonymous reports, track case status via secure case codes, and enabling moderators to manage workflow securely.",
        version: "0.1.0"
    },
    paths: {
        "/": {
            get: {
                summary: "Home",
                operationId: "home__get",
                responses: {
                    "200": {
                        description: "Successful Response",
                        content: {
                            "application/json": {
                                schema: {
                                    type: "object",
                                    properties: {
                                        message: {
                                            type: "string",
                                            example: "Welcome to WhistleDrop - Speak Without Being Seen"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/reports": {
            post: {
                summary: "Create Report",
                description: "Submit an anonymous report without creating an account or providing identity details.",
                operationId: "create_report_reports_post",
                requestBody: {
                    required: true,
                    content: {
                        "application/json": {
                            schema: {
                                $ref: "#/components/schemas/ReportCreate"
                            }
                        }
                    }
                },
                responses: {
                    "201": {
                        description: "Report received successfully",
                        content: {
                            "application/json": {
                                schema: {
                                    $ref: "#/components/schemas/ReportCreateResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        description: "Invalid category or validation error"
                    }
                }
            },
            get: {
                summary: "Get All Reports",
                description: "Moderator endpoint to view and filter reports. Requires `X-Moderator-Key` header.",
                operationId: "get_all_reports_reports_get",
                parameters: [
                    {
                        name: "category",
                        in: "query",
                        required: false,
                        schema: {
                            type: "string",
                            enum: ["Security", "Harassment", "Corruption", "Technical", "Other"]
                        }
                    },
                    {
                        name: "status",
                        in: "query",
                        required: false,
                        schema: {
                            type: "string",
                            enum: ["SUBMITTED", "UNDER_REVIEW", "RESOLVED", "DISMISSED"]
                        }
                    },
                    {
                        name: "X-Moderator-Key",
                        in: "header",
                        required: true,
                        schema: {
                            type: "string",
                            example: "WD-MOD-2026"
                        }
                    }
                ],
                responses: {
                    "200": {
                        description: "List of reports",
                        content: {
                            "application/json": {
                                schema: {
                                    type: "array",
                                    items: {
                                        $ref: "#/components/schemas/ReportModel"
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        description: "Unauthorized moderator access"
                    },
                    "400": {
                        description: "Invalid status"
                    }
                }
            }
        },
        "/reports/{case_code}": {
            get: {
                summary: "Get Report",
                description: "Track report status using unique case code. No login required.",
                operationId: "get_report_reports__case_code__get",
                parameters: [
                    {
                        name: "case_code",
                        in: "path",
                        required: true,
                        schema: {
                            type: "string",
                            example: "WD-A7K92M4QX81P"
                        }
                    }
                ],
                responses: {
                    "200": {
                        description: "Report details",
                        content: {
                            "application/json": {
                                schema: {
                                    $ref: "#/components/schemas/ReportModel"
                                }
                            }
                        }
                    },
                    "404": {
                        description: "Report not found"
                    }
                }
            }
        },
        "/reports/{case_code}/status": {
            put: {
                summary: "Update Status",
                description: "Update report status following valid transition workflow (SUBMITTED -> UNDER_REVIEW -> RESOLVED/DISMISSED). Requires `X-Moderator-Key` header.",
                operationId: "update_status_reports__case_code__status_put",
                parameters: [
                    {
                        name: "case_code",
                        in: "path",
                        required: true,
                        schema: {
                            type: "string",
                            example: "WD-A7K92M4QX81P"
                        }
                    },
                    {
                        name: "X-Moderator-Key",
                        in: "header",
                        required: true,
                        schema: {
                            type: "string",
                            example: "WD-MOD-2026"
                        }
                    }
                ],
                requestBody: {
                    required: true,
                    content: {
                        "application/json": {
                            schema: {
                                $ref: "#/components/schemas/StatusUpdate"
                            }
                        }
                    }
                },
                responses: {
                    "200": {
                        description: "Report status updated successfully",
                        content: {
                            "application/json": {
                                schema: {
                                    $ref: "#/components/schemas/StatusUpdateResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        description: "Invalid status or invalid status transition"
                    },
                    "401": {
                        description: "Unauthorized moderator access"
                    },
                    "404": {
                        description: "Report not found"
                    }
                }
            }
        }
    },
    components: {
        schemas: {
            ReportCreate: {
                type: "object",
                required: ["category", "description"],
                properties: {
                    category: {
                        type: "string",
                        enum: ["Security", "Harassment", "Corruption", "Technical", "Other"],
                        example: "Security"
                    },
                    description: {
                        type: "string",
                        minLength: 1,
                        example: "There is a security issue that needs to be reviewed."
                    },
                    evidence_url: {
                        type: "string",
                        nullable: true,
                        example: "https://example.com/evidence"
                    }
                }
            },
            ReportCreateResponse: {
                type: "object",
                properties: {
                    message: {
                        type: "string",
                        example: "Report received successfully"
                    },
                    case_code: {
                        type: "string",
                        example: "WD-A7K92M4QX81P"
                    },
                    category: {
                        type: "string",
                        example: "Security"
                    },
                    description: {
                        type: "string",
                        example: "There is a security issue that needs to be reviewed."
                    },
                    evidence_url: {
                        type: "string",
                        nullable: true,
                        example: "https://example.com/evidence"
                    }
                }
            },
            StatusUpdate: {
                type: "object",
                required: ["status"],
                properties: {
                    status: {
                        type: "string",
                        enum: ["SUBMITTED", "UNDER_REVIEW", "RESOLVED", "DISMISSED"],
                        example: "UNDER_REVIEW"
                    },
                    status_update: {
                        type: "string",
                        nullable: true,
                        example: "The report is currently being reviewed."
                    }
                }
            },
            StatusUpdateResponse: {
                type: "object",
                properties: {
                    message: {
                        type: "string",
                        example: "Report status updated successfully"
                    },
                    case_code: {
                        type: "string",
                        example: "WD-A7K92M4QX81P"
                    },
                    status: {
                        type: "string",
                        example: "UNDER_REVIEW"
                    },
                    status_update: {
                        type: "string",
                        nullable: true,
                        example: "The report is currently being reviewed."
                    }
                }
            },
            ReportModel: {
                type: "object",
                properties: {
                    id: {
                        type: "integer",
                        example: 1
                    },
                    case_code: {
                        type: "string",
                        example: "WD-A7K92M4QX81P"
                    },
                    category: {
                        type: "string",
                        example: "Security"
                    },
                    description: {
                        type: "string",
                        example: "There is a security issue that needs to be reviewed."
                    },
                    evidence_url: {
                        type: "string",
                        nullable: true,
                        example: "https://example.com/evidence"
                    },
                    status: {
                        type: "string",
                        example: "SUBMITTED"
                    },
                    status_update: {
                        type: "string",
                        nullable: true,
                        example: null
                    },
                    created_at: {
                        type: "string",
                        format: "date-time",
                        example: "2026-10-01T10:15:00.000Z"
                    }
                }
            }
        }
    }
};
