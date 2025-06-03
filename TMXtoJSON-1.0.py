import json
import os
import tkinter as tk
import traceback
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox, ttk



class HexagonLab:
    def __init__(self, root):
        self.root = root
        self.root.title("TMX to JSON Converter - 1.0 by HEXAGON-Lab")
        self.root.geometry("800x600")

        self.label = tk.Label(root, text="Select TMX file:")
        self.label.pack(pady=5)

        self.load_file_button = tk.Button(root, text="Upload file", command=self.load_file)
        self.load_file_button.pack(pady=5)

        self.lang_frame = tk.Frame(root)
        self.lang_frame.pack(pady=5)

        tk.Label(self.lang_frame, text="Source language:").grid(row=0, column=0, padx=5)
        self.src_lang_var = tk.StringVar()
        self.src_lang_dropdown = ttk.Combobox(self.lang_frame, textvariable=self.src_lang_var, width=10, state='readonly')
        self.src_lang_dropdown.grid(row=0, column=1)

        tk.Label(self.lang_frame, text="Target language:").grid(row=0, column=2, padx=5)
        self.tgt_lang_var = tk.StringVar()
        self.tgt_lang_dropdown = ttk.Combobox(self.lang_frame, textvariable=self.tgt_lang_var, width=10, state='readonly')
        self.tgt_lang_dropdown.grid(row=0, column=3)
        self.display_limit_var = tk.IntVar(value=100)
        tk.Label(root, text="Number of rows to visualize:").pack()
        self.display_limit_entry = tk.Entry(root, textvariable=self.display_limit_var, width=10)
        self.display_limit_entry.pack()
        self.display_limit_entry.bind("<Return>", lambda e: self.load_data())

        self.export_frame = tk.Frame(root)
        self.export_frame.pack(pady=5)

        self.export_buttons = {
            "JSON": ("JSON file", ".json", self.write_json),

        }

        self.export_buttons_widgets = {}
        for i, (label, (desc, ext, func)) in enumerate(self.export_buttons.items()):
            btn = tk.Button(self.export_frame, text=f"Export to {label}", command=lambda f=func, d=desc, e=ext: self.export_generic(d, e, f), state=tk.DISABLED)
            btn.grid(row=0, column=i, padx=2, pady=2)
            self.export_buttons_widgets[label] = btn

        text_frame = tk.Frame(root)
        text_frame.pack(pady=5, fill="both", expand=True)
        self.text = tk.Text(text_frame, height=20, width=100, wrap="word")
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(text_frame, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

        self.pairs = []
        self.file_paths = []


    def switch_languages(self):
        src = self.src_lang_var.get()
        tgt = self.tgt_lang_var.get()
        self.src_lang_var.set(tgt)
        self.tgt_lang_var.set(src)
        self.load_data()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[["TMX file", "*.tmx"]])
        if file_path:
            self.file_paths = [file_path]
            self.load_data()

    def load_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.file_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith(".tmx")]
            self.load_data()

    def load_data(self):
        if not self.file_paths:
            return

        self.text.delete(1.0, tk.END)
        self.pairs = []
        langs_found = set()

        for file_path in self.file_paths:
            try:
                tree = ET.parse(file_path)
                root_xml = tree.getroot()
                for tu in root_xml.iter("tu"):
                    for tuv in tu.findall("tuv"):
                        lang = tuv.attrib.get("{http://www.w3.org/XML/1998/namespace}lang") or tuv.attrib.get("lang")
                        if lang:
                            langs_found.add(lang.lower())
            except Exception as e:
                self.text.insert(tk.END, f"Error reading {file_path}: {str(e)}\n")
                continue

        sorted_langs = sorted(langs_found)
        self.src_lang_dropdown['values'] = sorted_langs
        self.tgt_lang_dropdown['values'] = sorted_langs

        if not sorted_langs:
            self.text.insert(tk.END, "No valid languages ​​found in the file(s).\n")
            return

        if not self.src_lang_var.get() or self.src_lang_var.get() not in sorted_langs:
            self.src_lang_var.set(sorted_langs[0])
        if not self.tgt_lang_var.get() or self.tgt_lang_var.get() not in sorted_langs:
            self.tgt_lang_var.set(sorted_langs[1] if len(sorted_langs) > 1 else '')

        self.text.insert(tk.END, f"Languages ​​found: {', '.join(sorted_langs)}\n\n")

        src_lang = self.src_lang_var.get().strip().lower()
        tgt_lang = self.tgt_lang_var.get().strip().lower()

        for file_path in self.file_paths:
            try:
                tree = ET.parse(file_path)
                root_xml = tree.getroot()
                for tu in root_xml.iter("tu"):
                    lang_map = {}
                    for tuv in tu.findall("tuv"):
                        lang = tuv.attrib.get("{http://www.w3.org/XML/1998/namespace}lang") or tuv.attrib.get("lang")
                        seg = tuv.find("seg")
                        if lang and seg is not None:
                            lang_map[lang.lower()] = seg.text
                    if src_lang in lang_map and tgt_lang in lang_map:
                        self.pairs.append((lang_map[src_lang], lang_map[tgt_lang]))
            except Exception as e:
                self.text.insert(tk.END, f"Error processing {file_path}: {str(e)}\n")
                continue

        if not self.pairs:
            self.text.insert(tk.END, "No pairs found.\n")
            for btn in self.export_buttons_widgets.values():
                btn.config(state=tk.DISABLED)
        else:
            display_limit = self.display_limit_var.get()
            for i, (src, tgt) in enumerate(self.pairs[:display_limit]):
                self.text.insert(tk.END, f"{i+1}. {src} -> {tgt}\n")
            for btn in self.export_buttons_widgets.values():
                btn.config(state=tk.NORMAL)

    def export_generic(self, filetype_desc, file_ext, write_function):
        if not self.pairs:
            messagebox.showinfo("Information", "No data to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=file_ext, filetypes=[(filetype_desc, f"*{file_ext}")])
        if not file_path:
            return
        try:
            write_function(file_path)
            messagebox.showinfo("Success", f"File successfully exported: {file_path}")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Export failed: {e}")



    def write_json(self, file_path):
        data = [{"source": src, "target": tgt} for src, tgt in self.pairs]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        root = tk.Tk()
        app = HexagonLab(root)
        root.mainloop()
    except Exception as e:
        print("Fatal error when starting the application:")
        traceback.print_exc()
        with open("tmx_error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)