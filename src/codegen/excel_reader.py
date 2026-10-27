"""
src/codegen/excel_reader.py
基本設計書（Excel形式: .xlsx）からセル情報を読み出し、LLMプロンプト用テキストへ変換する独立モジュール。
"""

from pathlib import Path
import openpyxl


def load_design_from_excel(file_path: str | Path) -> str:
    """
    Excel設計書（.xlsx）を開き、シートタイトルおよび行データをパイプ区切りテキストとして抽出。
    空行は自動スキップ。
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"設計書ファイルが存在しません: {path.resolve()}")

    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active

    extracted_lines = [f"【シート名: {ws.title}】"]
    for row in ws.iter_rows(values_only=True):
        non_empty = [str(cell).strip() for cell in row if cell is not None and str(cell).strip()]
        if non_empty:
            extracted_lines.append(" | ".join(non_empty))

    return "\n".join(extracted_lines)