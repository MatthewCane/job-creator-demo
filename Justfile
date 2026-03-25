synth:
  @uv run main.py

deploy:
  kubectl apply -f dist/ --namespace test-ns