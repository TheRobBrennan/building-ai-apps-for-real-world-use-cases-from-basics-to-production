"""
Tests for verify_environment.py
"""
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
import sys

# Create mock modules
numpy_mock = MagicMock(__version__='2.2.3')
ollama_mock = MagicMock()
gradio_mock = MagicMock(__version__='5.20.0')
jupyter_core_mock = MagicMock(__version__='5.7.2')

# Mock the imports before importing verify_environment
with patch.dict(sys.modules, {
    'numpy': numpy_mock,
    'ollama': ollama_mock,
    'gradio': gradio_mock,
    'jupyter_core': jupyter_core_mock
}):
    import verify_environment

@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks before each test"""
    numpy_mock.reset_mock()
    ollama_mock.reset_mock()
    gradio_mock.reset_mock()
    jupyter_core_mock.reset_mock()
    yield

@pytest.fixture
def mock_packages():
    with patch.dict(sys.modules, {
        'numpy': numpy_mock,
        'ollama': ollama_mock,
        'gradio': gradio_mock,
        'jupyter_core': jupyter_core_mock
    }):
        yield

@pytest.fixture
def mock_ollama_list():
    """Mock the actual models we have installed"""
    mock_models = []
    
    model1 = MagicMock()
    model1.model = "gemma2:2b"
    model1.size = 1.5 * 1024**3  # 1.5GB in bytes
    
    model2 = MagicMock()
    model2.model = "gemma2:2b-instruct-fp16"
    model2.size = 4.9 * 1024**3  # 4.9GB in bytes
    
    model3 = MagicMock()
    model3.model = "gemma2:2b-instruct-q2_K"
    model3.size = 1.1 * 1024**3  # 1.1GB in bytes
    
    mock_response = MagicMock()
    mock_response.models = [model1, model2, model3]
    
    ollama_mock.list = MagicMock(return_value=mock_response)
    yield
    ollama_mock.list.side_effect = None

@pytest.mark.asyncio
async def test_verify_ollama_models_found():
    """Test when all models are found"""
    # Create a mock response for ollama.list()
    mock_model = MagicMock()
    mock_model.model = "gemma2:2b"
    mock_model.size = 1.5 * 1024**3  # 1.5GB in bytes
    
    mock_model2 = MagicMock()
    mock_model2.model = "gemma2:2b-instruct-fp16"
    mock_model2.size = 4.9 * 1024**3
    
    mock_model3 = MagicMock()
    mock_model3.model = "gemma2:2b-instruct-q2_K"
    mock_model3.size = 1.1 * 1024**3
    
    mock_response = MagicMock()
    mock_response.models = [mock_model, mock_model2, mock_model3]
    ollama_mock.list = MagicMock(return_value=mock_response)
    
    with patch.dict(sys.modules, {'ollama': ollama_mock}):
        model_status = await verify_environment.verify_ollama_models()
    
    assert len(model_status) == 3
    assert all(status == "installed" for _, status, _ in model_status)
    assert "1.5GB" in model_status[0][2]
    assert "4.9GB" in model_status[1][2]
    assert "1.1GB" in model_status[2][2]

@pytest.mark.asyncio
async def test_verify_ollama_models_not_found():
    """Test when Ollama is not installed"""
    with patch.dict(sys.modules, {'ollama': None}):
        model_status = await verify_environment.verify_ollama_models()
    
    assert len(model_status) == 3
    assert all(status == "NOT FOUND" for _, status, _ in model_status)

@pytest.mark.asyncio
async def test_verify_ollama_models_list_error():
    """Test when Ollama list() raises an error"""
    # Reset all mocks to ensure clean state
    ollama_mock.reset_mock()
    ollama_mock.list = MagicMock(side_effect=Exception("Test error"))
    
    with patch.dict(sys.modules, {'ollama': ollama_mock}):
        model_status = await verify_environment.verify_ollama_models()
    
    # Verify all models are marked as not found
    assert len(model_status) == 3
    assert all(status == "NOT FOUND" for _, status, _ in model_status)

def test_verify_dependencies_all_found(mock_packages):
    """Test when all packages are found"""
    packages = verify_environment.verify_dependencies()
    assert len(packages) == 4
    assert all(version != "NOT FOUND" for _, version in packages)
    assert any(pkg == "numpy" and ver == "2.2.3" for pkg, ver in packages)

def test_verify_dependencies_not_found():
    """Test when packages are not found"""
    with patch.dict(sys.modules, {
        'numpy': None,
        'ollama': None,
        'gradio': None,
        'jupyter_core': None
    }):
        packages = verify_environment.verify_dependencies()
        assert len(packages) == 4
        assert all(version == "NOT FOUND" for _, version in packages)

def test_verify_dependencies_jupyter_not_found():
    """Test when jupyter_core specifically is not found"""
    with patch.dict(sys.modules, {
        'numpy': numpy_mock,
        'ollama': ollama_mock,
        'gradio': gradio_mock,
        'jupyter_core': None
    }):
        packages = verify_environment.verify_dependencies()
        assert len(packages) == 4
        assert any(pkg == "jupyter" and ver == "NOT FOUND" for pkg, ver in packages)

def test_verify_dependencies_jupyter_import_error():
    """Test when jupyter_core raises ImportError"""
    mock_jupyter = MagicMock()
    # Make __version__ raise ImportError when accessed
    type(mock_jupyter).__version__ = PropertyMock(side_effect=ImportError())
    
    with patch.dict(sys.modules, {
        'numpy': numpy_mock,
        'ollama': ollama_mock,
        'gradio': gradio_mock,
        'jupyter_core': mock_jupyter
    }):
        packages = verify_environment.verify_dependencies()
        assert len(packages) == 4
        assert any(pkg == "jupyter" and ver == "NOT FOUND" for pkg, ver in packages)

def test_main_execution():
    """Test direct script execution"""
    # Save the original __name__
    original_name = verify_environment.__name__
    try:
        # Set __name__ to '__main__' to simulate direct script execution
        verify_environment.__name__ = '__main__'
        # Re-execute the main block
        if verify_environment.__name__ == '__main__':
            verify_environment.main()
    finally:
        # Restore the original __name__
        verify_environment.__name__ = original_name

def test_main_function(capsys, mock_packages):
    """Test the main function output"""
    # Create mock response for ollama.list()
    mock_model = MagicMock()
    mock_model.model = "gemma2:2b"
    mock_model.size = 1.5 * 1024**3
    
    mock_model2 = MagicMock()
    mock_model2.model = "gemma2:2b-instruct-fp16"
    mock_model2.size = 4.9 * 1024**3
    
    mock_model3 = MagicMock()
    mock_model3.model = "gemma2:2b-instruct-q2_K"
    mock_model3.size = 1.1 * 1024**3
    
    mock_response = MagicMock()
    mock_response.models = [mock_model, mock_model2, mock_model3]
    ollama_mock.list = MagicMock(return_value=mock_response)
    
    verify_environment.main()
    captured = capsys.readouterr()
    
    # Test success path
    assert "AI Basics Workshop - Package Verification" in captured.out
    assert "Checking required packages..." in captured.out
    assert "Checking required Ollama models..." in captured.out
    assert "✨ All requirements are satisfied!" in captured.out
    
    # Test missing packages path
    with patch.dict(sys.modules, {
        'numpy': None,
        'ollama': ollama_mock,
        'gradio': gradio_mock,
        'jupyter_core': jupyter_core_mock
    }):
        verify_environment.main()
        captured = capsys.readouterr()
        assert "⚠️  Some requirements are missing:" in captured.out
        assert "Install missing packages: pip install -r requirements.txt" in captured.out
        assert "❌ numpy: NOT FOUND" in captured.out
    
    # Test missing models path
    ollama_mock.list = MagicMock(side_effect=Exception("Test error"))
    verify_environment.main()
    captured = capsys.readouterr()
    assert "⚠️  Some requirements are missing:" in captured.out
    assert "Install missing models:" in captured.out
    assert "ollama pull gemma2:2b" in captured.out
    assert "ollama pull gemma2:2b-instruct-fp16" in captured.out
    assert "ollama pull gemma2:2b-instruct-q2_K" in captured.out 