#!/usr/bin/env python3
"""
واجهة سطر الأوامر لـ MOFNet
"""

import argparse
import sys
from . import calculate_pri, classify_pri_level

def main():
    parser = argparse.ArgumentParser(
        description="MOFNet - نظام التنبؤ بفشل الأعضاء المتعدد",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  %(prog)s --hr 80 --sbp 120 --dbp 80 --rr 16 --spo2 98
  %(prog)s --file patients.csv
        """
    )
    
    parser.add_argument('--hr', type=int, help='معدل ضربات القلب')
    parser.add_argument('--sbp', type=int, help='الضغط الانقباضي')
    parser.add_argument('--dbp', type=int, help='الضغط الانبساطي')
    parser.add_argument('--rr', type=int, help='معدل التنفس')
    parser.add_argument('--spo2', type=int, help='تشبع الأكسجين')
    parser.add_argument('--file', type=str, help='ملف CSV للمرضى')
    parser.add_argument('--version', action='store_true', help='عرض الإصدار')
    
    args = parser.parse_args()
    
    if args.version:
        from . import __version__
        print(f"MOFNet v{__version__}")
        return
    
    if all([args.hr, args.sbp, args.dbp, args.rr, args.spo2]):
        pri = calculate_pri(args.hr, args.sbp, args.dbp, args.rr, args.spo2)
        classification = classify_pri_level(pri)
        
        print("📊 نتيجة التحليل:")
        print(f"  مؤشر PRI: {pri:.3f}")
        print(f"  التصنيف: {classification}")
        print(f"  الحالة: {'🟢 جيدة' if pri > 0.7 else '🟡 متوسطة' if pri > 0.5 else '🔴 حرجة'}")
    
    elif args.file:
        print(f"🔬 تحليل ملف: {args.file}")
        # هنا يمكن إضافة كود تحليل CSV
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
