"""
LLM client using IBM watsonx.ai — same setup as procedurko.

Reads from env vars:
  WATSONX_API_KEY, WATSONX_URL, WATSONX_PROJECT_ID, LLM_MODEL_ID
"""
import os
from langchain_ibm import ChatWatsonx
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams


def _build_llm(max_tokens: int, temperature: float) -> ChatWatsonx:
    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: max_tokens,
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.TEMPERATURE: temperature,
    }
    return ChatWatsonx(
        model_id=os.environ.get("LLM_MODEL_ID", "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"),
        url=os.environ.get("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com"),
        apikey=os.environ.get("WATSONX_API_KEY", ""),
        project_id=os.environ.get("WATSONX_PROJECT_ID", ""),
        params=params,
    )


def get_fast_llm() -> ChatWatsonx:
    """For intermediate nodes — collector, curator, briefings, query gen."""
    return _build_llm(max_tokens=1024, temperature=0.0)


def get_smart_llm() -> ChatWatsonx:
    """For final editor and validator passes."""
    return _build_llm(max_tokens=4096, temperature=0.2)
