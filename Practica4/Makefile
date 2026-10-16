PYTHON ?= python
EMCC ?= emcc
WAT2WASM ?= wat2wasm

PY_SCRIPTS = oneaddr.py stackvm.py regvm.py codec.py

.PHONY: all python wasm clean serve

all: python wasm

python:
	@echo "=== oneaddr.py ==="
	$(PYTHON) oneaddr.py
	@echo "\n=== stackvm.py ==="
	$(PYTHON) stackvm.py
	@echo "\n=== regvm.py ==="
	$(PYTHON) regvm.py
	@echo "\n=== codec.py ==="
	$(PYTHON) codec.py

wasm: wasm/sum.wasm wasm/sum2.wasm

wasm/sum.wasm: wasm/sum.c
	emcc wasm/sum.c -O3 -s WASM=1 -s EXPORTED_FUNCTIONS='["_S"]' -s STANDALONE_WASM=1 --no-entry -o wasm/sum.wasm

wasm/sum2.wasm: wasm/sum.wat
	@echo "=== sum.wat -> sum2.wasm ==="
	$(WAT2WASM) wasm/sum.wat -o wasm/sum2.wasm

serve:
	@echo "Запуск сервера на http://localhost:8000"
	cd wasm && $(PYTHON) -m http.server

clean:
	@echo "=== Очистка сгенерированных файлов ==="
	rm -f wasm/sum.wasm wasm/sum2.wasm sum.bin
	# Для Windows cmd используй: del /Q wasm\sum.wasm wasm\sum2.wasm sum.bin