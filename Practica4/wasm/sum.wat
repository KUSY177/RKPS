(module
  (import "env" "prompt" (func $prompt (result i32)))
  (import "env" "alert" (func $alert (param i32)))
  (func $main (export "main")
    (local $sum i32)
    (local $num i32)
    (local.set $sum (i32.const 0))
    (block $done
      (loop $loop
        (local.set $num (call $prompt))
        (br_if $done (i32.eqz (local.get $num)))
        (local.set $sum (i32.add (local.get $sum) (local.get $num)))
        (br $loop)
      )
    )
    (call $alert (local.get $sum))
  )
)