import os
import sys
import ctypes

def ensure_env_configured():
    """Ensure OpenMP (libomp) and C runtime libraries are preloaded on macOS/Linux."""
    if sys.platform == "darwin":
        candidate_paths = [
            "/opt/anaconda3/lib/libomp.dylib",
            "/opt/anaconda3/pkgs/llvm-openmp-20.1.8-he822017_0/lib/libomp.dylib",
            "/opt/homebrew/opt/libomp/lib/libomp.dylib",
            "/usr/local/opt/libomp/lib/libomp.dylib",
            "/usr/local/lib/libomp.dylib",
            os.path.expanduser("~/anaconda3/lib/libomp.dylib"),
            os.path.expanduser("~/miniconda3/lib/libomp.dylib"),
        ]
        for path in candidate_paths:
            if os.path.exists(path):
                try:
                    ctypes.CDLL(path)
                    break
                except Exception:
                    pass

        # Also populate DYLD paths if available
        for lib_dir in ["/opt/anaconda3/lib", "/opt/homebrew/opt/libomp/lib", "/usr/local/opt/libomp/lib"]:
            if os.path.exists(lib_dir):
                if "DYLD_LIBRARY_PATH" in os.environ:
                    if lib_dir not in os.environ["DYLD_LIBRARY_PATH"]:
                        os.environ["DYLD_LIBRARY_PATH"] = f"{lib_dir}:{os.environ['DYLD_LIBRARY_PATH']}"
                else:
                    os.environ["DYLD_LIBRARY_PATH"] = lib_dir

# Run on import
ensure_env_configured()
