# Project Brief

## Project Title
SCD2 Copilot

## Problem Statement
Enterprise teams repeatedly hand-code Slowly Changing Dimension Type 2 (SCD2) logic for data warehouse tables. This is repetitive, error-prone, and hard to maintain.

## Goal
Build a tool that:
- takes today's source CSV
- takes yesterday's SCD2 CSV
- detects new / updated / unchanged / deleted records
- generates the new SCD2 table
- validates correctness
- explains every change in natural language

## Why It Matters
SCD2 is used in enterprise analytics, compliance, audit trails, and historical reporting. Current platforms partially automate it, but teams still spend time managing keys, dates, merges, and edge cases.

## Project Value
This project should feel like a real business tool:
- useful for analysts and data engineers
- explainable for business users
- deployable as a web app
- testable and trustworthy

## Primary Users
- Data engineers
- Analytics engineers
- Warehouse teams
- Business stakeholders reviewing historical changes

## Success Criteria
- Correct SCD2 output
- Clear validation results
- Clear change explanations
- Public demo deployment
- Clean docs and tests

## Non-Goals
- Full ETL platform
- Multi-tenant SaaS
- Large-scale distributed compute
- Multi-agent AI swarm
- Custom MCP server in MVP