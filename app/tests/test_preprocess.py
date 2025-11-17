from app.data_pipeline.preprocess_pipeline import PreprocessPipeline

def test_pipeline():
    pipeline = PreprocessPipeline("app/tests/sample_resume.pdf")
    output = pipeline.run()

    assert "clean_text" in output
    assert "skills" in output
    assert isinstance(output["skills"], list)

