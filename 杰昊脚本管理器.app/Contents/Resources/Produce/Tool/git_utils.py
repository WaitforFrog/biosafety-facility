"""
Git 提交推送工具
"""
import os
import subprocess
import time


def git_commit_and_push(commit_message, build_script_path=None):
    """自动提交并推送到远程仓库"""
    try:
        if build_script_path and os.path.exists(build_script_path):
            print(f"\n🔄 正在更新所有产品的文章索引页...")
            result = subprocess.run(
                ["python3", build_script_path],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"  ✅ 文章索引更新完成")
            else:
                print(f"  ⚠️ 文章索引更新失败: {result.stderr}")

        print(f"\n🔄 正在 git add...")
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)

        print(f"📝 正在 git commit...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True)

        print(f"🚀 正在推送到远程仓库...")
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    ["git", "push"],
                    check=True,
                    capture_output=True,
                    timeout=120
                )
                print(f"✅ Git 提交并推送成功!")
                return True
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode() if e.stderr else str(e)
                if attempt < max_retries - 1:
                    print(f"⚠️  Push 尝试 {attempt + 1} 失败，{retry_delay}秒后重试... ({error_msg[:100]})")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"❌ Git 操作失败: {error_msg}")
                    return False
            except subprocess.TimeoutExpired:
                if attempt < max_retries - 1:
                    print(f"⚠️  Push 超时，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"❌ Git 操作失败: 超时")
                    return False
            except Exception as e:
                print(f"❌ Git 操作异常: {e}")
                return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"❌ Git 操作异常: {e}")
        return False
