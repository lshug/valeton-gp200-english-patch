#!/usr/bin/env python3
"""
Generate English translations for Valeton GP-200 firmware strings.
This script provides context-aware translations for guitar processor UI strings.
"""

import json

# Domain-specific translations for guitar effects processor
# These are carefully crafted for the limited display space on the device

TRANSLATIONS: dict[str, str] = {
    # === Simplified Chinese ===
    # Version/System info
    "硬件版本 ": "HW Ver ",
    "固件版本 ": "FW Ver ",
    " 箭 ": " Arr",  # Shortened for byte alignment
    "踏板 ": "Pedal ",
    # System messages
    "系统过载\n请尝试调整您的效果链 !": "System Overload!\nAdjust FX Chain!",
    "警告!": "Warn!",  # Shortened for byte alignment
    "数据重置中,\n请勿关闭电源！": "Resetting...\nDO NOT POWER OFF!",
    "恢复成功！": "Reset OK!",
    # Input/Output channels
    "输入通道(USB)": "Input Ch(USB)",
    "输出通道(USB)": "Output Ch(USB)",
    "时钟输出(USB)": "Clk Out(USB)",  # Shortened for byte alignment
    "输入通道(TRS)": "Input Ch(TRS)",
    "输出通道(TRS)": "Output Ch(TRS)",
    "时钟输出(TRS)": "Clk Out(TRS)",  # Shortened for byte alignment
    # Cabinet modes
    "无箱体模式(L)": "No CAB Mode(L)",
    "无箱体模式(R)": "No CAB Mode(R)",
    "CAB自动跟随": "CAB Match",
    # Preset navigation
    "预设组+": "Bank+",
    "预设组-": "Bank-",
    "预设+": "Prst+",  # Shortened for byte alignment
    "预设-": "Prst-",  # Shortened for byte alignment
    "预设组": "Bank",
    "预设": "Prst",  # Shortened for byte alignment
    "预选": "Prvw",  # Shortened for byte alignment
    # Drum machine
    "鼓机预设+": "Drum+",
    "鼓机预设-": "Drum-",
    "鼓机": "Drum",
    "鼓机速度": "DrumBPM",  # Shortened for byte alignment
    "鼓机同步": "Drm Sync",  # Shortened for byte alignment
    "按下鼓机键\n播放/暂停鼓机\n按下或旋转PARA旋钮\n选择类型": "Press DRUM key\nPlay/Pause\nRotate PARA\nSelect Type",
    # Footswitches
    "脚钉10": "FS 10",
    "脚钉 1": "FS 1",
    "脚钉 2": "FS 2",
    "脚钉 3": "FS 3",
    "脚钉 4": "FS 4",
    "脚钉 5": "FS 5",
    "脚钉 6": "FS 6",
    "脚钉 7": "FS 7",
    "脚钉 8": "FS 8",
    "脚钉9": "FS 9",
    "脚钉 1+2": "FS 1+2",
    "脚钉 2+3": "FS 2+3",
    "脚钉 3+4": "FS 3+4",
    "脚钉 3/4": "FS 3/4",
    "脚钉 1+5": "FS 1+5",
    "脚钉 5+6": "FS 5+6",
    "脚钉 6+7": "FS 6+7",
    "脚钉 7+8": "FS 7+8",
    "脚钉": "FS",
    "外接脚钉1": "ExtFS 1",  # Shortened for byte alignment
    "外接脚钉2": "ExtFS 2",  # Shortened for byte alignment
    "外接脚钉3": "ExtFS 3",  # Shortened for byte alignment
    "外接脚钉4": "ExtFS 4",  # Shortened for byte alignment
    "双脚钉": "Dual FS",
    "单脚钉": "Singl FS",  # Shortened for byte alignment
    "脚钉数据重置": "FS Reset",  # Shortened for byte alignment
    # Expression pedals
    "踏板1": "EXP 1",
    "踏板2": "EXP 2",
    "踏板1-A": "EXP 1-A",
    "踏板1-B": "EXP 1-B",
    "踏板 1 A/B": "EXP 1 A/B",
    "外接踏板/脚钉": "Ext EXP/FS",
    "踏板设置": "Pedal Set",
    # Knobs and parameters
    "快调旋钮 1": "Knob 1",
    "快调旋钮 2": "Knob 2",
    "快调旋钮 3": "Knob 3",
    "快调旋钮1-3": "Knob1-3",  # Shortened for byte alignment
    "参数 1": "Param 1",
    "参数 2": "Param 2",
    "参数 3": "Param 3",
    "参数": "Para",  # Shortened for byte alignment
    "按下PARA旋钮以编辑。": "Press PARA to Edit",
    "按下PARA旋钮确认进入": "Press PARA to Enter",
    "按下PARA旋钮进行下一步": "Press PARA to Continue",
    # EQ bands
    "频段 1 Q": "Band 1 Q",
    "频段 2 Q": "Band 2 Q",
    "频段 3 Q": "Band 3 Q",
    "频段 4 Q": "Band 4 Q",
    "频段 1 频率": "Band1 Frq",  # Shortened for byte alignment
    "频段 2 频率": "Band2 Frq",  # Shortened for byte alignment
    "频段 3 频率": "Band3 Frq",  # Shortened for byte alignment
    "频段 4 频率": "Band4 Frq",  # Shortened for byte alignment
    "频段 1 增益": "Band1 Gn",  # Shortened for byte alignment
    "频段 2 增益": "Band2 Gn",  # Shortened for byte alignment
    "频段 3 增益": "Band3 Gn",  # Shortened for byte alignment
    "频段 4 增益": "Band4 Gn",  # Shortened for byte alignment
    "全局EQ": "Glbl EQ",  # Shortened for byte alignment
    "低切": "LoCut",  # Shortened for byte alignment
    "高切": "HiCut",  # Shortened for byte alignment
    # Audio modes
    "仅USB": "USB",  # Shortened for byte alignment
    "仅TRS": "TRS",  # Shortened for byte alignment
    "Aux接入USB": "Aux to USB",
    "USB音频": "USB Aud",  # Shortened for byte alignment
    "USB模式": "USB Mode",
    "通道": "Ch",  # Shortened for byte alignment
    "左声道": "Left Ch",
    "右声道": "Right Ch",
    # Language
    "语言": "Lang",  # Shortened for byte alignment
    "中文": "CN",  # Shortened for byte alignment
    "页码": "Page",
    # Reference frequency
    "参考频率": "Ref Freq",
    # UI elements
    "光标": "Curs",  # Shortened for byte alignment
    "混合": "Mix",  # Shortened for byte alignment
    "取消": "Cncl",  # Shortened for byte alignment
    "确定": "OK",
    "返回": "Back",
    "退出": "Exit",
    "删除": "Del",  # Shortened for byte alignment
    "存储": "Save",
    "移动": "Move",
    "字符": "Chr",  # Shortened for byte alignment
    "显示": "Disp",  # Shortened for byte alignment
    "空": "--",  # Shortened for byte alignment
    "风格": "Styl",  # Shortened for byte alignment
    "数据": "Data",
    "命令": "Cmd",  # Shortened for byte alignment
    # Copyright
    "©Valeton 版权所有": "(C)Valeton",
    # Factory reset options
    "恢复原厂预设（01-A~25-D）": "Reset Presets(01-A~25-D)",
    "恢复所有内容（删除所有用户存储的数据并恢复到出厂状态）": "Reset All Data",
    "恢复全局设置": "Rst Global",
    "恢复出厂设置": "Factory Rst",
    "执行此操作会恢复原厂预设（01-A~25-D）至出厂默认状态,\n是否继续？": "Reset Presets?\nContinue?",
    "执行此操作会恢复全部数据至出厂默认状态,\n是否继续？": "Reset All Data?\nContinue?",
    "执行此操作会恢复全局设置至出厂默认状态,\n是否继续？": "Reset Global?\nContinue?",
    "重置本页设置\n确定继续吗？": "Reset Page?\nContinue?",
    # Input gain
    "输入增益": "In Gain",
    # Actions
    "按下": "Press",
    "踩下": "Step",
    "将踏板完全放下": "Press EXP",
    "将踏板完全抬起": "Lift EXP",
    "用力踩踏板前端": "Press Toe",
    "踩任意踩钉开启效果": "Any FS",
    # About
    "关于": "About",
    # Volume settings
    "预设声像": "Prst Pan",  # Shortened for byte alignment
    "发送量": "Send Lv",  # Shortened for byte alignment
    "返回量": "Retn Lv",  # Shortened for byte alignment
    "监听音量": "Mon Vol",  # Shortened for byte alignment
    "录音音量": "Rec Vol",
    "播放音量": "Play Vol",
    # Interface modes
    " 接口 1  模式": "Jack1 Mode",
    " 接口 2  模式": "Jack2 Mode",
    "自定义模式": "Custom Md",
    "选择一种恢复模式": "Select Mode",
    # Operating modes
    "单块模式": "Stomp Md",
    "传统模式": "Classic Md",
    "预设组切换模式": "Bank Sw",
    "输入模式": "Input Md",
    "正常模式": "Normal Md",
    "显示模式": "Disp Mode",
    "预设模式": "Preset Md",
    "模式": "Mode",
    # Calibration
    "校正完成": "Cal OK",
    "校正失败": "Cal Fail",
    # Clock/MIDI
    "时钟源": "Clk Src",
    "MIDI信号源": "MIDI Src",
    # Reverse
    "1/2    反向": "1/2 Rev",
    "反向": "Rev",
    # Serial/Parallel
    "并联/串联": "Para/Ser",
    "串联": "Ser",
    "并联": "Para",
    # Guitar types
    "原声吉他": "Acoustic",
    "电吉他": "Elec",
    # Module selection
    "选择模块": "Sel Mod",
    "模块": "Mod",
    # Bypass
    "已旁通": "Bypassed",
    "旁通": "Byps",
    # Undo/Redo
    "撤销    重做": "Undo Redo",
    # Effects
    "当前效果": "Curr FX",
    "效果": "FX",
    "效果回路": "FX Loop",
    "效果开关": "FX Sw",
    "开关": "Sw",
    # Tap tempo
    "打点定速": "Tap BPM",
    "分钟": "Min",
    # Stop
    "停止": "Stop",
    # Pedal calibration
    "踏板校正": "EXP Calib",
    # Line input
    "线性输入": "Line In",
    # Speed
    "1/2速度": "1/2 Spd",
    "预设速度": "Prst BPM",
    # Brightness
    "屏幕亮度": "Bright",
    # Auto
    "自动": "Auto",
    # Tuner
    "调音表": "Tuner",
    # Long press
    "长踩": "Hold",
    # On/Off
    "关闭": "Off",
    "开启": "On",
    # Recording
    "录制中": "Rec",
    "播放中": "Play",
    "自动录音": "Auto Rec",
    "无录制": "No Rec",
    "录制时长": "Rec Len",
    # Always on
    "常亮": "On",
    # Internal/External
    "内置": "Int",
    "外置": "Ext",
    # Pre/Post
    "前置": "Pre",
    "后置": "Post",
    "前置/后置": "Pre/Post",
    "发送位置": "Send Pos",
    "返回位置": "Return Pos",
    # Settings
    "CTRL设置": "CTRL Set",
    "全局设置": "Glbl Set",
    "预设设置": "Prst Set",
    "设置": "Setup",
    # Looper
    "乐句循环": "Looper",
    # Mute
    "静音": "Mute",
    # Wet/Dry
    "效果音": "Wet",
    "干音": "Dry",
    # Display time
    "显示时间": "Disp Tim",
    # Real-time
    "实时": "Live",
    # I/O
    "输入/输出": "Input/Output",
    # Min/Max
    "最小值": "Min",
    "最大值": "Max",
    # Signal chain
    "移动信号链": "Mv Chain",
    "信号链": "Chain",
    # Pedal
    "踏板": "EXP",
    # === Traditional Chinese ===
    "韌體版本 ": "FW Ver ",
    "硬體版本 ": "HW Ver ",
    "輸入通道(USB)": "Input Ch(USB)",
    "輸出通道(USB)": "Output Ch(USB)",
    "時序輸出(USB)": "Clock Out(USB)",
    "輸入通道(TRS)": "Input Ch(TRS)",
    "輸出通道(TRS)": "Output Ch(TRS)",
    "時序輸出(TRS)": "Clock Out(TRS)",
    "重置原廠設定(01-A~25-D)": "Reset Presets",
    "無箱體模式(左)": "No CAB Mode(L)",
    "無箱體模式(右)": "No CAB Mode(R)",
    "重置所有資料（所有使用者資料將會流失)": "Reset All Data",
    "音色群組+": "Bank+",
    "音色群組-": "Bank-",
    "音色群組": "Bank",
    "鼓組預設+": "Drum+",
    "鼓組預設-": "Drum-",
    "記憶音色+": "Preset+",
    "記憶音色-": "Preset-",
    "記憶音色": "Preset",
    "腳踏 10": "FS 10",
    "腳踏 1": "FS 1",
    "腳踏 2": "FS 2",
    "腳踏 3": "FS 3",
    "腳踏 4": "FS 4",
    "腳踏 5": "FS 5",
    "腳踏 6": "FS 6",
    "腳踏 7": "FS 7",
    "腳踏 8": "FS 8",
    "腳踏 9": "FS 9",
    "腳踏 1+2": "FS 1+2",
    "腳踏 2+3": "FS 2+3",
    "腳踏 3+4": "FS 3+4",
    "腳踏3/4": "FS 3/4",
    "腳踏 1+5": "FS 1+5",
    "腳踏 5+6": "FS 5+6",
    "腳踏 6+7": "FS 6+7",
    "腳踏 7+8": "FS 7+8",
    "旋鈕 1": "Knob 1",
    "旋鈕 2": "Knob 2",
    "旋鈕 3": "Knob 3",
    "旋鈕1-3": "Knob 1-3",
    "外部腳踏開關 1": "Ext FS 1",
    "外部腳踏開關 2": "Ext FS 2",
    "外部腳踏開關 3": "Ext FS 3",
    "外部腳踏開關 4": "Ext FS 4",
    "控制 1": "CTRL 1",
    "控制 2": "CTRL 2",
    "控制 3": "CTRL 3",
    "控制 4": "CTRL 4",
    "控制 5": "CTRL 5",
    "控制 6": "CTRL 6",
    "控制 7": "CTRL 7",
    "控制 8": "CTRL 8",
    "參數 1": "Param 1",
    "參數  2": "Param 2",
    "參數  3": "Param 3",
    "參數": "Para",
    "表情踏板 1": "EXP 1",
    "踏板 2": "EXP 2",
    "踏板 1-A": "EXP 1-A",
    "踏板 1-B": "EXP 1-B",
    "踏板1 A/B": "EXP 1 A/B",
    "僅 USB": "USB",
    "僅 TRS": "TRS",
    "輔助輸入到USB": "Aux to USB",
    "語言": "Lang",
    "恢復原廠設定中請勿關閉電源！": "Resetting...\nDO NOT POWER OFF!",
    "選擇模組": "Sel Module",
    "模組": "Mod",
    "訊號鏈管理": "Chain Setup",
    "訊號鍊": "Chain",
    "頻段1 頻率": "Band 1 Freq",
    "頻段2 頻率": "Band 2 Freq",
    "頻段3 頻率": "Band 3 Freq",
    "頻段4 頻率": "Band 4 Freq",
    "頻段1 增益": "Band 1 Gain",
    "頻段2 增益": "Band 2 Gain",
    "頻段3 增益": "Band 3 Gain",
    "頻段4 增益": "Band 4 Gain",
    "頻段1 等化器": "Band 1 EQ",
    "頻段2 等化器": "Band 2 EQ",
    "頻段3 等化器": "Band 3 EQ",
    "頻段4 等化器": "Band 4 EQ",
    "繁體中文": "TW",
    "系統過載 請嘗試重整您的效果器鏈": "System Overload!",
    "開啟/關閉": "On/Off",
    "將踏板完全關閉": "Press Pedal Fully",
    "將踏板完全打開": "Lift Pedal Fully",
    "將踏板用力踩下": "Press Pedal Hard",
    "關閉": "Off",
    "開啟": "On",
    "Valeton 版權所有": "(C) Valeton",
    "類型": "Type",
    "按下PARA以繼續": "Press PARA",
    "字母": "Char",
    "喇叭單體自動配對": "CAB Auto Match",
    "預設相位": "Preset Pan",
    "通過": "Pass",
    "輸入增益量": "Input Gain",
    "預設音量": "Prst Vol",
    "预设音量": "Prst Vol",
    "音量": "Vol",
    "预设音量/速度": "Vol/BPM",
    "錄音音量": "Rec Vol",
    "監聽音量": "Monitor Vol",
    "送出量": "Send Lv",
    "表情踏板/開關 1 模式": "EXP/FS 1 Mode",
    "表情踏板/開關 2 模式": "EXP/FS 2 Mode",
    "USB 模式": "USB Mode",
    "選擇一模式": "Select Mode",
    "使用者模式": "User Mode",
    "單顆模式": "Stomp Mode",
    "群組切換模式": "Bank Switch",
    "輸入模式": "Input Mode",
    "預設模式": "Preset Mode",
    "傳統模式": "Classic",
    "顯示模式": "Disp Mode",
    "時序源": "Clk Src",
    "MIDI訊號源": "MIDI Source",
    "左聲道": "Left Ch",
    "右聲道": "Right Ch",
    "錄音時間": "Rec Tim",
    "顯示時間": "Disp Tim",
    "短壓": "Tap",
    "長壓": "Hold",
    "移動": "Move",
    "木吉他": "Acoustic",
    "電吉他": "Electric",
    "校正失敗": "Cal Fail",
    "分鐘": "Min",
    "儲存": "Save",
    "游標": "Curs",
    "撤銷    重做": "Undo    Redo",
    "外觀設定": "Disp Setup",
    "恢復原廠設定": "Factory Reset",
    "預設設定": "Prst Setup",
    "僅重置總設定": "Reset Global Only",
    "總設定": "Global",
    "設定": "Setup",
    "確定": "OK",
    "前級/後級": "Pre/Post",
    "後級": "Post",
    "前級": "Pre",
    "即時切換": "Instant Sw",
    "預覽切換": "Preview Sw",
    "表情踏板/腳踏開關": "EXP/FS",
    "腳踏開關": "Footswitch",
    "效果開關": "FX Switch",
    "目前效果": "Current FX",
    "任意踩踏釘開啟效果": "Press Any FS",
    "恢復原廠設定成功": "Reset OK!",
    "鼓機": "Drum",
    "關於本機": "About",
    "重置設定 \n確定繼續？": "Reset Setup?\nContinue?",
    "此操作將清除所有使用者設定的資料\n是否繼續？": "Reset All Data?\nContinue?",
    "此操作將會將(01-A~25-D）恢復至原廠設定\n是否繼續？": "Reset Presets?\nContinue?",
    "此操作會將總設定恢復至原廠設定\n是否繼續？": "Reset Global?\nContinue?",
    "無": "--",
    "頁面": "Page",
    "刪除": "Del",
    "按下參數鈕進入": "Press PARA",
    "導線輸入": "Line Input",
    "鼓機同步": "Drm Sync",
    "打點速度": "Tap BPM",
    "鼓機速度": "Drm BPM",
    "螢幕亮度": "Bright",
    "內部": "Int",
    "調音器": "Tuner",
    "節拍器": "Metrnome",
    "高頻降噪": "High Cut",
    "低頻降噪": "Low Cut",
    "錄製中": "Rec",
    "發送位置": "Send Pos",
    "重置本頁踩釘設置": "Reset FS Setup",
    "控制設置": "CTRL Setup",
    "踏板設置": "Pedal Setup",
    "串聯": "Ser",
    "並聯": "Para",
    "並聯/串聯": "Para/Serial",
    "效果迴路": "FX Loop",
    "樂句循環": "Looper",
    "自動錄音": "Auto Record",
    "清音": "Clean",
    "靜音": "Mute",
    "輸入/輸出": "Input/Output",
    "USB音頻": "USB Aud",
    "音頻": "Audio",
    "風格": "Styl",
    "無錄製": "No Rec",
    "設定總覽": "Setup",
    "雙踏板": "Dual EXP",
    "單踏板": "Sngl EXP",
    # === Japanese ===
    "録音モード(L)": "Rec Mode(L)",
    "録音モード(R)": "Rec Mode(R)",
    "外部フットスイッチ1": "Ext FS 1",
    "外部フットスイッチ2": "Ext FS 2",
    "外部フットスイッチ3": "Ext FS 3",
    "外部フットスイッチ4": "Ext FS 4",
    "ファクトリーリセットが完了しました。": "Reset Complete!",
    "常時": "Alway",
    "分": "M",
    "信号経路の管理": "Chain Setup",
    "完了": "Done",
    "選択エフェクト": "Select FX",
    "バンク切替モード": "Bank Switch",
    "ペダルをヒールポ\nジションに上げる": "Lift Pedal\nFully Up",
    "閉じる": "Close",
    "戻る": "Back",
    "PARAを押して続行": "Press PARA",
    "事前/事後": "Pre/Post",
    "事後": "Post",
    "空き": "---",
    "事前": "Pre",
    "録音時間": "Rec Tim",
    "明るさ": "Bright",
    "元に戻す やり直し": "Undo Redo",
    "並列": "Para",
    "並列/直列": "Para/Serial",
    "直列": "Ser",
    "失敗": "Fail",
    "文字": "Char",
    "いずれかのフットスイッチを押す": "Press Any FS",
    "EXP動作範囲の設定": "EXP Range Setup",
    "PARAを押して決定": "Press PARA to OK",
    "入出力": "I/O",
    "モジュールを選択": "Select Module",
    "入力選択": "Input Sel",
    "オプションの選択": "Select Option",
    "言語": "Lang",
    "日本語": "JA",
    "同期": "Sync",
    "パッチ01-A~25-Dがデフォルト設定に変更されます。\n続行しますか？": "Reset Presets?\nContinue?",
    "グローバル設定がデフォルト設定に変更されます。\n続行しますか？": "Reset Global?\nContinue?",
    "ユーザーデータが消去されます。\n続行しますか？": "Reset User Data?\nContinue?",
    "再生ボリューム": "Play Vol",
    "録音ボリューム": "Rec Vol",
    "待つ": "Wait",
    "本機について": "About",
    "内部": "Int",
    "外部": "Ext",
    "入力レベル": "Input Level",
    "録音レベル": "Rec Level",
    "信号経路": "Chain",
    "システムオーバーフロー\n再セティングを試みる エフェクトチェーン": "System Overload!\nAdjust FX Chain",
    "自動録音": "Auto Record",
    "消去": "Del",
    "全データのリセット(全てのユーザーデータが消去されます)": "Reset All Data",
    "強く踏む": "Press Hard",
    "ペダルをつま\n先まで踏み込む": "Press Pedal\nFully Down",
    "リセット進行中　電源を切らないでください。": "Resetting...\nDO NOT POWER OFF!",
}


def apply_translations(input_file: str, output_file: str) -> None:
    """Apply translations to the JSON file."""
    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)

    translated_count = 0
    still_placeholder = 0

    for key in data:
        if key in TRANSLATIONS:
            data[key] = TRANSLATIONS[key]
            translated_count += 1
        elif data[key] == "PLACEHOLDER":
            still_placeholder += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Applied {translated_count} translations")
    print(f"Remaining placeholders: {still_placeholder}")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "translations_gp200.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    apply_translations(input_file, output_file)
