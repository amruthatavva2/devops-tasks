{{- define "projectpulse.name" -}}projectpulse{{- end -}}
{{- define "projectpulse.labels" -}}app.kubernetes.io/name: {{ include "projectpulse.name" . }}{{- end -}}
