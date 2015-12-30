handle all nostop
set sharedlibrary load-rules ".*" ".*" none
set inferior-auto-start-dyld off
set sharedlibrary preload-libraries off
set sharedlibrary load-dyld-symbols off
break *{{ entry_point }}
command 1
dump memory {{ binaryname }}.dec {{ start }} {{ end }}
end
run
