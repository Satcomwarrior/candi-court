125 for a in ns.attach:
126     argv += ["--attach", a]
127 if ns.dry_run:
128     argv.append("--dry-run")
129 sys.argv = ["automate_intake_email.py"] + argv
130 intake_main()
131 p5.set_defaults(func=_cmd_intake)
132
133 p6 = sub.add_parser("powershell", help="Run a PowerShell script from powershell/")
134 p6.add_argument("script", help="Script filename in powershell/")
135 p6.add_argument("psargs", nargs=argparse.REMAINDER, help="Arguments passed to PowerShell (prefix with --)")
136 p6.set_defaults(func=cmd_powershell)
137
138 p7 = sub.add_parser("generate-docs", help="Generate Snohomish templates into filled documents")
139 p7.add_argument("--input", required=True, help="Path to case data JSON")
140 p7.add_argument("--output-dir", default=str(Path("outputs") / "generated_docs"))
141 p7.add_argument("--only", nargs="*", choices=["motion", "declaration", "contempt"], help="Limit which docs")
142 def _cmd_gen(ns):
143     from scripts.generate_case_documents import main as gen_main
144     argv = ["--input", ns.input, "--output-dir", ns.output_dir]
145     if ns.only:
146         argv += ["--only", *ns.only]
147     import sys as _sys
148     _sys.argv = ["generate_case_documents.py"] + argv
149     gen_main()
150 p7.set_defaults(func=_cmd_gen)
151
152 p8 = sub.add_parser("screen-analysis", help="Run screen recording analysis with OCR")
153 p8.add_argument("--screen-recordings", help="Directory of screen recording video files")
154 p8.add_argument("--screenshots", help="Directory of screenshot images")
155 p8.add_argument("--transcripts", help="Directory containing transcript or OCR sidecar text files")
156 p8.add_argument("--output-dir", default="media_analysis_output", help="Directory for generated analysis artifacts")
157 p8.add_argument("--frame-interval", type=float, default=10.0, help="Seconds between sampled frames for OCR")
158 p8.add_argument("--max-frames", type=int, default=8, help="Maximum frames to OCR per video")
159 p8.add_argument("--skip-audio", action="store_true", help="Disable audio transcription attempts")
160 p8.add_argument("--skip-video-ocr", action="store_true", help="Disable OCR sampling from video frames")
161 p8.add_argument("--skip-screenshot-ocr", action="store_true", help="Disable OCR on screenshots")
162 p8.add_argument("--whisper-model", default="base", help="Whisper model size to use when enabled")
163 p8.add_argument("--force", action="store_true", help="Remove existing output directory before running")
164
165 def _cmd_screen(ns):
166     from pathlib import Path as _Path
167     from media_analysis import AnalysisOptions, run_media_analysis
168
169     options = AnalysisOptions(
170         enable_audio_transcription=not ns.skip_audio,
171         enable_video_ocr=not ns.skip_video_ocr,
172         enable_screenshot_ocr=not ns.skip_screenshot_ocr,
173         frame_interval_seconds=ns.frame_interval,
174         whisper_model=ns.whisper_model,
175         max_frames=ns.max_frames,
176     )
177
178     run_media_analysis(
179         screen_recordings_dir=_Path(ns.screen_recordings) if ns.screen_recordings else None,
180         screenshots_dir=_Path(ns.screenshots) if ns.screenshots else None,
181         transcripts_dir=_Path(ns.transcripts) if ns.transcripts else None,
182         output_dir=_Path(ns.output_dir),
183         options=options,
184         force=ns.force,
185     )
186
187 p8.set_defaults(func=_cmd_screen)
188 p9 = sub.add_parser("full", help="Run the full workflow end-to-end")
189 p9.add_argument("--case-data", default=str(Path("case_data.sample.json")), help="Path to case data JSON")
190 p9.add_argument("--output-dir", default=str(Path("outputs") / "generated_docs"))
191 p9.add_argument("--send-intake", action="store_true", help="Actually send intake emails (omit for dry-run)")
192 p9.add_argument("--ps-script", help="Optional PowerShell script from powershell/ to run at the end")
193 p9.add_argument("--psargs", nargs=argparse.REMAINDER, help="Args passed to the PowerShell script (prefix with --)")
194
195 def _cmd_full(ns):
196     # 1) Forms + templates (skip if Snohomish templates already exist)
197     try:
198         snohomish_dir = Path("templates/family_law_forms/snohomish_county")
199         def _valid(p): return p.exists() and p.stat().st_size > 1000
200         required = [
201             snohomish_dir / "template_motion_modify_custody_and_parenting_plan.txt",
202             snohomish_dir / "template_declaration_modify_custody_and_parenting_plan.txt",
203             snohomish_dir / "template_contempt_motion.txt",
204         ]
205         if all(_valid(p) for p in required):
206             print("[INFO] Templates already present; skipping forms download.")
207         else:
208             try:
209                 # Try regenerating templates only (cheap)
210                 from download_family_law_forms import WashingtonFormsDownloader
211                 dl = WashingtonFormsDownloader()
212                 dl.create_snohomish_county_templates()
213                 print("[INFO] Recreated Snohomish templates.")
214             except Exception:
215                 # As a fallback, attempt full forms download if space permits
216                 from download_family_law_forms import WashingtonFormsDownloader
217                 dl = WashingtonFormsDownloader()
218                 stats = dl.download_all_forms()
219                 dl.create_snohomish_county_templates()
220                 dl.save_download_log()
221                 dl.generate_summary_report(stats)
222     except Exception as e:
223         print(f"[WARN] Forms step failed: {e}")
224
225     # 2) Generate documents
226     try:
227         from scripts.generate_case_documents import main as gen_main
228         argv = ["--input", ns.case_data, "--output-dir", ns.output_dir]
229         import sys as _sys
230         _sys.argv = ["generate_case_documents.py"] + argv
231         gen_main()
232     except Exception as e:
233         print(f"[WARN] Document generation failed: {e}")
234
235     # 3) Intake email (dry-run unless flagged)
236     try:
237         body_path = Path("intake_email_draft.txt")
238         if not body_path.exists():
239             print("[INFO] Skipping intake email: intake_email_draft.txt not found.")
240         else:
241             from automation.automate_intake_email import main as intake_main
242             argv = ["--body", str(body_path)]
243             if not ns.send_intake:
244                 argv.append("--dry-run")
245             import sys as _sys
246             _sys.argv = ["automate_intake_email.py"] + argv
247             intake_main()
248     except Exception as e:
249         print(f"[WARN] Intake email step failed: {e}")
250
251     # 4) Optional PowerShell orchestrator
252     if ns.ps_script:
253         try:
254             _args = argparse.Namespace(script=ns.ps_script, psargs=ns.psargs or [])
255             cmd_powershell(_args)
256         except SystemExit as se:
257             raise
258         except Exception as e:
259             print(f"[WARN] PowerShell step failed: {e}")
260
261 p9.set_defaults(func=_cmd_full)
262
263 args = ap.parse_args()
264 args.func(args)
265
266
267 if __name__ == "__main__":
268     main()