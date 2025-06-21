import os
import uuid
import ddddocr
from selenium.webdriver.common.by import By


# 解壓縮檔案
def extract_archive(archive_path: str, output_dir: str):
    print(f"✅ 解壓完成：{archive_path} → {output_dir}")


def get_verification_code(path):
    ocr = ddddocr.DdddOcr()
    with open(path, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    os.remove(path)
    return res


# 圖像辨識驗證碼
def get_v_code(driver, image_xpath):
    v_path = str(uuid.uuid1()) + 'v.png'
    driver.find_element(By.XPATH, image_xpath).screenshot(v_path)
    return get_verification_code(v_path)


def pack_chrome_extension(extension_dir: str, pem_path: str) -> str:
    """
    自動封裝 Chrome 擴充功能為 .crx，並使用提供的私鑰（.pem），回傳產生的擴充功能 ID
    :param extension_dir: 擴充功能資料夾（內含 manifest.json）
    :param pem_path: 私鑰檔案路徑（.pem）
    :return: Chrome 擴充功能 ID
    """
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # macOS Chrome 路徑

    if not os.path.exists(extension_dir):
        raise FileNotFoundError("❌ 擴充功能資料夾不存在")

    if not os.path.exists(pem_path):
        raise FileNotFoundError("❌ 私鑰檔案不存在")

    cmd = [
        chrome_path,
        f"--pack-extension={extension_dir}",
        f"--pack-extension-key={pem_path}"
    ]

    print("🚀 封裝中：", " ".join(cmd))
    subprocess.run(cmd)

    print("✅ 封裝完成！")

    # 回傳 extension ID
    return get_chrome_extension_id(pem_path)
