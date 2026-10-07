{{- define "webapp.name" -}}webapp{{- end }}
{{- define "webapp.fullname" -}}{{ .Release.Name }}-{{ include "webapp.name" . }}{{- end }}
