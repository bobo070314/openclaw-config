import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))

import pytest
import subprocess
import pathlib
from unittest.mock import patch, mock_open, MagicMock

from igp_mcp_bridge import IGP_MCP  # Replace 'your_module' with actual module name


class TestIGP_MCP:
    def test_init_with_workdir(self, tmp_path):
        workdir = tmp_path / "test_workspace"
        mcp = IGP_MCP(workdir=str(workdir))
        assert mcp.workdir == workdir

    def test_init_default_workdir(self):
        mcp = IGP_MCP()
        assert isinstance(mcp.workdir, pathlib.Path)

    def test_read_file_exists(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world", encoding="utf-8")
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.read_file("test.txt")
        assert result == "hello world"

    def test_read_file_not_exists(self, tmp_path):
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.read_file("missing.txt")
        assert result.startswith("ERROR: 文件不存在:")

    def test_write_file_creates_dirs(self, tmp_path):
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.write_file("subdir/nested.txt", "content")
        assert result.startswith("OK: 写入")
        written = tmp_path / "subdir" / "nested.txt"
        assert written.exists()
        assert written.read_text(encoding="utf-8") == "content"

    def test_edit_file_success(self, tmp_path):
        test_file = tmp_path / "edit.txt"
        test_file.write_text("old content", encoding="utf-8")
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.edit_file("edit.txt", "old", "new")
        assert result.startswith("OK: 替换成功")
        assert test_file.read_text(encoding="utf-8") == "new content"

    def test_edit_file_not_found(self, tmp_path):
        test_file = tmp_path / "edit.txt"
        test_file.write_text("no match here", encoding="utf-8")
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.edit_file("edit.txt", "missing", "new")
        assert result.startswith("ERROR: 未找到匹配文本:")

    def test_edit_file_multiple_matches(self, tmp_path):
        test_file = tmp_path / "edit.txt"
        test_file.write_text("old old", encoding="utf-8")
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.edit_file("edit.txt", "old", "new")
        assert result.startswith("ERROR: 找到2处匹配,需要唯一匹配")

    @patch("subprocess.run")
    def test_shell_local_exec_success(self, mock_run, tmp_path):
        mock_run.return_value = MagicMock(stdout="output", stderr="", returncode=0)
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.shell("echo hello")
        assert result == "output"

    @patch("subprocess.run")
    def test_shell_local_exec_failure(self, mock_run, tmp_path):
        mock_run.return_value = MagicMock(stdout="", stderr="error", returncode=1)
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.shell("false")
        assert result == "error"

    @patch("subprocess.run")
    def test_git_status_success(self, mock_run, tmp_path):
        mock_run.return_value = MagicMock(stdout=" M file.txt", stderr="", returncode=0)
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.git_status(".")
        assert result == " M file.txt"

    @patch("subprocess.run")
    def test_git_diff_success(self, mock_run, tmp_path):
        mock_run.return_value = MagicMock(stdout="diff content", stderr="", returncode=0)
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.git_diff(".")
        assert result == "diff content"

    @patch("subprocess.run")
    def test_git_commit_success(self, mock_run, tmp_path):
        mock_run.return_value = MagicMock(stdout="committed", stderr="", returncode=0)
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.git_commit(".", "test msg")
        assert "committed" in result

    def test_ls_directory(self, tmp_path):
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "file.txt").write_text("x")
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.ls(".")
        lines = result.strip().split("\n")
        assert len(lines) == 2
        assert any("D subdir" in line for line in lines)
        assert any("F file.txt" in line for line in lines)

    def test_ls_not_directory(self, tmp_path):
        test_file = tmp_path / "not_dir.txt"
        test_file.write_text("x")
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.ls("not_dir.txt")
        assert result.startswith("ERROR: 不是目录:")

    @patch("pathlib.Path.rglob")
    def test_glob_success(self, mock_rglob, tmp_path):
        mock_rglob.return_value = [tmp_path / "match1.txt", tmp_path / "match2.py"]
        mcp = IGP_MCP(workdir=tmp_path)
        result = mcp.glob("*.txt")
        assert "match1.txt" in result
        assert "match2.py" not in result