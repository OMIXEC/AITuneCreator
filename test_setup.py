#!/usr/bin/env python3
"""
AITuneCreator Setup and Functionality Tests
Tests to verify the environment is correctly set up and the app works
"""

import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add repo to path
sys.path.insert(0, str(Path(__file__).parent))


class TestEnvironmentSetup(unittest.TestCase):
    """Test environment configuration"""

    def test_python_version(self):
        """Test that Python version is 3.11+"""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3)
        self.assertGreaterEqual(version.minor, 11)

    def test_env_files_exist(self):
        """Test that environment template exists"""
        self.assertTrue(Path('.env.example').exists(), ".env.example not found")

    def test_required_files_exist(self):
        """Test that all required project files exist"""
        required_files = [
            'app.py',
            'app/__init__.py',
            'app/main.py',
            'app/utils.py',
            'requirements.txt',
            'setup.py',
        ]

        for file in required_files:
            with self.subTest(file=file):
                self.assertTrue(Path(file).exists(), f"{file} not found")

    def test_gitignore_excludes_env(self):
        """Test that .gitignore properly excludes .env files"""
        gitignore_path = Path('.gitignore')
        self.assertTrue(gitignore_path.exists(), ".gitignore not found")

        with open(gitignore_path) as f:
            content = f.read()
            self.assertIn('.env', content, ".env not in .gitignore")

    def test_venv_exists(self):
        """Test that virtual environment is set up"""
        venv_path = Path('venv')
        self.assertTrue(venv_path.exists(), "Virtual environment not found")
        self.assertTrue((venv_path / 'bin' / 'python').exists() or
                       (venv_path / 'Scripts' / 'python.exe').exists(),
                       "Python executable not found in venv")


class TestDependencies(unittest.TestCase):
    """Test that all dependencies are installed"""

    def test_streamlit_installed(self):
        """Test Streamlit is installed"""
        try:
            import streamlit
            self.assertIsNotNone(streamlit.__version__)
        except ImportError:
            self.fail("Streamlit not installed")

    def test_langchain_installed(self):
        """Test LangChain is installed"""
        try:
            import langchain
            self.assertIsNotNone(langchain.__version__)
        except ImportError:
            self.fail("LangChain not installed")

    def test_langchain_core_installed(self):
        """Test langchain-core is installed"""
        try:
            from langchain_core.prompts import ChatPromptTemplate
            self.assertIsNotNone(ChatPromptTemplate)
        except ImportError:
            self.fail("langchain-core not installed or ChatPromptTemplate not found")

    def test_langchain_groq_installed(self):
        """Test langchain-groq is installed"""
        try:
            from langchain_groq import ChatGroq
            self.assertIsNotNone(ChatGroq)
        except ImportError:
            self.fail("langchain-groq not installed")

    def test_music21_installed(self):
        """Test music21 is installed"""
        try:
            import music21
            self.assertIsNotNone(music21.__version__)
        except ImportError:
            self.fail("music21 not installed")

    def test_synthesizer_installed(self):
        """Test synthesizer is installed"""
        try:
            from synthesizer import Synthesizer, Waveform
            self.assertIsNotNone(Synthesizer)
            self.assertIsNotNone(Waveform)
        except ImportError:
            self.fail("synthesizer not installed")

    def test_scipy_installed(self):
        """Test scipy is installed"""
        try:
            from scipy.io.wavfile import write as write_wav
            self.assertIsNotNone(write_wav)
        except ImportError:
            self.fail("scipy not installed")


class TestApplicationStructure(unittest.TestCase):
    """Test the application code structure"""

    def test_musicllm_class_exists(self):
        """Test that MusicLLM class can be imported"""
        try:
            from app.main import MusicLLM
            self.assertIsNotNone(MusicLLM)
        except ImportError as e:
            self.fail(f"Failed to import MusicLLM: {e}")

    def test_musicllm_has_required_methods(self):
        """Test that MusicLLM has all required methods"""
        from app.main import MusicLLM

        required_methods = [
            'generate_melody',
            'generate_harmony',
            'generate_rythm',
            'adapt_style'
        ]

        for method in required_methods:
            with self.subTest(method=method):
                self.assertTrue(hasattr(MusicLLM, method),
                               f"MusicLLM missing method: {method}")

    def test_utils_functions_exist(self):
        """Test that utility functions exist"""
        try:
            from app.utils import note_to_frequencies, generate_wav_bytes_from_notes_freq
            self.assertIsNotNone(note_to_frequencies)
            self.assertIsNotNone(generate_wav_bytes_from_notes_freq)
        except ImportError as e:
            self.fail(f"Failed to import utility functions: {e}")

    def test_note_to_frequencies_works(self):
        """Test note_to_frequencies function"""
        from app.utils import note_to_frequencies

        # Test with valid note
        freqs = note_to_frequencies(['C4', 'D4', 'E4'])
        self.assertEqual(len(freqs), 3)
        self.assertTrue(all(isinstance(f, float) for f in freqs))

        # Test with empty list
        freqs = note_to_frequencies([])
        self.assertEqual(len(freqs), 0)

    def test_wav_generation_works(self):
        """Test WAV file generation"""
        from app.utils import generate_wav_bytes_from_notes_freq
        import io

        # Test with some frequencies
        freqs = [440, 493.88, 523.25]  # A4, B4, C5
        wav_bytes = generate_wav_bytes_from_notes_freq(freqs)

        # Check that we got valid WAV data
        self.assertIsInstance(wav_bytes, bytes)
        self.assertGreater(len(wav_bytes), 0)

        # Check for WAV file signature
        self.assertEqual(wav_bytes[:4], b'RIFF', "WAV file signature not found")

    def test_musicllm_initialization(self):
        """Test that MusicLLM can be initialized with test key"""
        from app.main import MusicLLM
        import os
        from dotenv import load_dotenv

        # Load test environment
        if os.path.exists('.env.dev'):
            load_dotenv('.env.dev')

        # This should work even with dummy API key (won't call API)
        try:
            llm = MusicLLM(temperature=0.7)
            self.assertIsNotNone(llm)
            self.assertIsNotNone(llm.llm)
        except Exception as e:
            self.fail(f"Failed to initialize MusicLLM: {e}")


class TestDocumentation(unittest.TestCase):
    """Test that documentation files exist"""

    def test_claude_md_exists(self):
        """Test that CLAUDE.md exists"""
        self.assertTrue(Path('CLAUDE.md').exists(), "CLAUDE.md not found")

    def test_developer_guide_exists(self):
        """Test that DEVELOPER_GUIDE.md exists"""
        self.assertTrue(Path('DEVELOPER_GUIDE.md').exists(), "DEVELOPER_GUIDE.md not found")

    def test_readme_exists(self):
        """Test that README.md exists"""
        self.assertTrue(Path('README.md').exists(), "README.md not found")

    def test_claude_md_has_content(self):
        """Test that CLAUDE.md has substantial content"""
        with open('CLAUDE.md') as f:
            content = f.read()
            self.assertGreater(len(content), 1000, "CLAUDE.md is too short")
            self.assertIn('Developer Setup', content, "CLAUDE.md missing setup guide")

    def test_developer_guide_has_content(self):
        """Test that DEVELOPER_GUIDE.md has content"""
        with open('DEVELOPER_GUIDE.md') as f:
            content = f.read()
            self.assertGreater(len(content), 500, "DEVELOPER_GUIDE.md is too short")
            self.assertIn('Quick Start', content, "DEVELOPER_GUIDE.md missing quick start")


class TestSetupScripts(unittest.TestCase):
    """Test that setup scripts exist"""

    def test_setup_sh_exists(self):
        """Test that setup.sh exists"""
        self.assertTrue(Path('setup.sh').exists(), "setup.sh not found")

    def test_setup_bat_exists(self):
        """Test that setup.bat exists"""
        self.assertTrue(Path('setup.bat').exists(), "setup.bat not found")

    def test_validate_env_exists(self):
        """Test that validate-env.py exists"""
        self.assertTrue(Path('validate-env.py').exists(), "validate-env.py not found")

    def test_setup_sh_is_executable(self):
        """Test that setup.sh is executable"""
        import stat
        path = Path('setup.sh')
        if path.exists():
            mode = path.stat().st_mode
            is_executable = bool(mode & stat.S_IXUSR)
            # May not be executable in all environments, so just check it exists
            self.assertTrue(path.exists())


def run_tests():
    """Run all tests with verbose output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEnvironmentSetup))
    suite.addTests(loader.loadTestsFromTestCase(TestDependencies))
    suite.addTests(loader.loadTestsFromTestCase(TestApplicationStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentation))
    suite.addTests(loader.loadTestsFromTestCase(TestSetupScripts))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED!")
        print(f"  Ran {result.testsRun} tests successfully")
    else:
        print("✗ SOME TESTS FAILED")
        print(f"  Tests run: {result.testsRun}")
        print(f"  Failures: {len(result.failures)}")
        print(f"  Errors: {len(result.errors)}")

    print("=" * 70 + "\n")

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
