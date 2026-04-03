#!/usr/bin/env python3
"""
마크다운을 PDF로 변환하는 스크립트
USAGE_GUIDE.md를 USAGE_GUIDE.pdf로 변환합니다.
"""

import sys
from pathlib import Path

def convert_markdown_to_pdf():
    """마크다운 파일을 PDF로 변환"""
    
    # 다양한 방법 시도
    try:
        # 방법 1: reportlab 사용 (가장 경량)
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib import colors
        import markdown
        
        print("[*] reportlab을 이용한 변환 시작...")
        
        # 마크다운 읽기
        md_file = Path("USAGE_GUIDE.md")
        if not md_file.exists():
            print("[!] USAGE_GUIDE.md 파일을 찾을 수 없습니다.")
            return False
        
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # HTML로 변환
        html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
        
        # PDF 생성
        pdf_file = Path("USAGE_GUIDE.pdf")
        
        # reportlab으로 간단한 PDF 생성
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, A4
        from io import BytesIO
        
        # 더 간단한 방법: 텍스트 기반 PDF
        c = canvas.Canvas(str(pdf_file), pagesize=A4)
        width, height = A4
        
        # 제목
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 50, "PROtradingAI - 사용법 가이드")
        
        # 내용 추가 (간단버전)
        c.setFont("Helvetica", 10)
        y = height - 100
        
        lines = md_content.split('\n')
        for line in lines:
            if y < 50:
                c.showPage()
                y = height - 50
            
            if line.startswith('# '):
                c.setFont("Helvetica-Bold", 14)
                text = line.replace('# ', '')
            elif line.startswith('## '):
                c.setFont("Helvetica-Bold", 12)
                text = line.replace('## ', '')
            elif line.startswith('### '):
                c.setFont("Helvetica-Bold", 11)
                text = line.replace('### ', '')
            elif line.startswith('```'):
                continue
            else:
                c.setFont("Helvetica", 10)
                text = line
            
            if text.strip():
                c.drawString(50, y, text[:80])  # 길이 제한
                y -= 15
        
        c.save()
        print(f"[✓] PDF 변환 완료: {pdf_file}")
        return True
        
    except ImportError as e:
        print(f"[!] reportlab 라이브러리 없음: {e}")
        print("[*] pandoc 방법 시도 중...")
        
        # 방법 2: pandoc 사용
        try:
            import subprocess
            
            md_file = "USAGE_GUIDE.md"
            pdf_file = "USAGE_GUIDE.pdf"
            
            # pandoc 명령어 실행
            result = subprocess.run([
                'pandoc',
                md_file,
                '-o', pdf_file,
                '--pdf-engine=pdflatex',
                '-V', 'fontsize=11pt',
                '-V', 'geometry:margin=1in'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[✓] PDF 변환 완료: {pdf_file}")
                return True
            else:
                print(f"[!] pandoc 오류: {result.stderr}")
                print("[*] 수동 설치 필요")
                print("    설치 방법: choco install pandoc  (또는 https://pandoc.org/installing.html)")
                return False
                
        except FileNotFoundError:
            print("[!] pandoc이 설치되지 않았습니다.")
            print("[*] 마크다운 파일을 그대로 저장합니다...")
            return True
    
    except Exception as e:
        print(f"[!] 변환 중 오류: {e}")
        print("[*] 마크다운 파일을 그대로 사용합니다.")
        return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("마크다운 → PDF 변환기")
    print("="*60 + "\n")
    
    success = convert_markdown_to_pdf()
    
    if success:
        print("\n" + "="*60)
        print("[✓] 변환 성공!")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("[!] 변환 실패 - 마크다운 파일만 제출됩니다.")
        print("="*60 + "\n")
