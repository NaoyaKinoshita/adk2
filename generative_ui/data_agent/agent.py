import google.auth
from google.adk import Agent
from google.adk.integrations.bigquery import (
    BigQueryCredentialsConfig,
    BigQueryToolset,
)
from google.adk.integrations.bigquery.config import BigQueryToolConfig, WriteMode
from google.adk.models import Gemini
from google.genai import types

from data_agent.callbacks import stash_query_result
from data_agent.config import (
    BQ_APPLICATION_NAME,
    BQ_COMPUTE_PROJECT_ID,
    BQ_DATASET,
    BQ_LOCATION,
    BQ_MAX_RESULT_ROWS,
    BQ_MAXIMUM_BYTES_BILLED,
    BQ_TOOL_NAMES,
    GEMINI_MODEL,
    LLM_RETRY_OPTIONS,
    LLM_TIMEOUT_MS,
)
from data_agent.models import QueryResultSummary
from data_agent.prompts import data_agent_instruction

# Application Default Credentials (ローカルは gcloud auth application-default login)
credentials, _ = google.auth.default()

bigquery_toolset = BigQueryToolset(
    tool_filter=BQ_TOOL_NAMES,
    credentials_config=BigQueryCredentialsConfig(credentials=credentials),
    bigquery_tool_config=BigQueryToolConfig(
        # 書き込み系のクエリはツール側で拒否する
        write_mode=WriteMode.BLOCKED,
        max_query_result_rows=BQ_MAX_RESULT_ROWS,
        maximum_bytes_billed=BQ_MAXIMUM_BYTES_BILLED,
        compute_project_id=BQ_COMPUTE_PROJECT_ID,
        location=BQ_LOCATION,
        application_name=BQ_APPLICATION_NAME,
    ),
)

data_agent = Agent(
    name="data_agent",
    description="自然言語の依頼を BigQuery の SQL に変換して実行し、結果の result_id と要約を返す",
    model=Gemini(model=GEMINI_MODEL, retry_options=LLM_RETRY_OPTIONS),
    instruction=data_agent_instruction(BQ_DATASET),
    tools=[bigquery_toolset],
    after_tool_callback=stash_query_result,
    output_schema=QueryResultSummary,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(timeout=LLM_TIMEOUT_MS),
    ),
)

# adk web data_agent 単体で動作確認できるようにする
root_agent = data_agent
