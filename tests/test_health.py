import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.models.job_spec import JobSpecification, RubricWeights, StrictnessLevel


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_settings_loaded():
    settings = get_settings()
    assert settings.app_name == "Enterprise-Candidate-Intelligence-Screener"
    assert settings.max_recursion_limit == 10
    assert settings.default_strictness == "balanced"


def test_rubric_weights_validation():
    # Valid weights (sum = 1.0)
    valid_weights = RubricWeights(skills=0.6, experience=0.2, domain_education=0.2)
    assert valid_weights.skills == 0.6

    # Invalid weights (sum != 1.0)
    with pytest.raises(ValueError):
        RubricWeights(skills=0.8, experience=0.5, domain_education=0.2)


def test_canonical_job_spec():
    job = JobSpecification(
        title="Senior Backend Engineer",
        min_experience_years=3.5,
        must_have_skills=["Java", "Distributed Systems", "Kafka"],
        good_to_have_skills=["Kubernetes", "AWS"],
        strictness_level=StrictnessLevel.STRICT,
    )
    assert job.title == "Senior Backend Engineer"
    assert len(job.must_have_skills) == 3
    assert job.strictness_level == StrictnessLevel.STRICT


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data


def test_health_check_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "gemini_configured" in data

