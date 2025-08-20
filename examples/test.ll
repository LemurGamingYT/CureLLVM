; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

%"Ref" = type {i8*, i8* (i8*)*, i64}
%"string" = type {i8*, i64, %"Ref"*}
define i32 @"main"()
{
entry:
  %".2" = call %"string" @"string.new"(i8* getelementptr ([47 x i8], [47 x i8]* @"str", i32 0, i32 0), i32 47)
  %".3" = extractvalue %"string" %".2", 2
  %".4" = call i8* @"Ref.inc"(%"Ref"* %".3")
  %"memory_var" = alloca %"string"
  store %"string" %".2", %"string"* %"memory_var"
  %"temp_mem" = load %"string", %"string"* %"memory_var"
  %".6" = call %"string" @"input_prompt"(%"string" %"temp_mem")
  %".7" = extractvalue %"string" %".6", 2
  %".8" = call i8* @"Ref.inc"(%"Ref"* %".7")
  %"memory_var.1" = alloca %"string"
  store %"string" %".6", %"string"* %"memory_var.1"
  %"temp_mem.1" = load %"string", %"string"* %"memory_var.1"
  %"area_ptr" = alloca float
  store float              0x0, float* %"area_ptr"
  %".11" = call %"string" @"string.new"(i8* getelementptr ([7 x i8], [7 x i8]* @"str.2", i32 0, i32 0), i32 6)
  %".12" = extractvalue %"string" %".11", 2
  %".13" = call i8* @"Ref.inc"(%"Ref"* %".12")
  %"memory_var.2" = alloca %"string"
  store %"string" %".11", %"string"* %"memory_var.2"
  %"temp_mem.2" = load %"string", %"string"* %"memory_var.2"
  %".15" = call i1 @"string.eq_string"(%"string" %"temp_mem.1", %"string" %"temp_mem.2")
  br i1 %".15", label %"if_then", label %"elif_test_0"
if_merge:
  %".113" = call %"string" @"string.new"(i8* getelementptr ([7 x i8], [7 x i8]* @"str.10", i32 0, i32 0), i32 6)
  %".114" = extractvalue %"string" %".113", 2
  %".115" = call i8* @"Ref.inc"(%"Ref"* %".114")
  %"memory_var.14" = alloca %"string"
  store %"string" %".113", %"string"* %"memory_var.14"
  %"temp_mem.14" = load %"string", %"string"* %"memory_var.14"
  %"area" = load float, float* %"area_ptr"
  %".117" = call %"string" @"float.to_string"(float %"area")
  %".118" = extractvalue %"string" %".117", 2
  %".119" = call i8* @"Ref.inc"(%"Ref"* %".118")
  %"memory_var.15" = alloca %"string"
  store %"string" %".117", %"string"* %"memory_var.15"
  %"temp_mem.15" = load %"string", %"string"* %"memory_var.15"
  %".121" = call %"string" @"string.add_string"(%"string" %"temp_mem.14", %"string" %"temp_mem.15")
  %".122" = extractvalue %"string" %".121", 2
  %".123" = call i8* @"Ref.inc"(%"Ref"* %".122")
  %"memory_var.16" = alloca %"string"
  store %"string" %".121", %"string"* %"memory_var.16"
  %"temp_mem.16" = load %"string", %"string"* %"memory_var.16"
  %".125" = call i8* @"print_string"(%"string" %"temp_mem.16")
  br label %"cleanup.4"
if_then:
  %".17" = call %"string" @"string.new"(i8* getelementptr ([31 x i8], [31 x i8]* @"str.3", i32 0, i32 0), i32 30)
  %".18" = extractvalue %"string" %".17", 2
  %".19" = call i8* @"Ref.inc"(%"Ref"* %".18")
  %"memory_var.3" = alloca %"string"
  store %"string" %".17", %"string"* %"memory_var.3"
  %"temp_mem.3" = load %"string", %"string"* %"memory_var.3"
  %".21" = call %"string" @"input_prompt"(%"string" %"temp_mem.3")
  %".22" = extractvalue %"string" %".21", 2
  %".23" = call i8* @"Ref.inc"(%"Ref"* %".22")
  %"memory_var.4" = alloca %"string"
  store %"string" %".21", %"string"* %"memory_var.4"
  %"temp_mem.4" = load %"string", %"string"* %"memory_var.4"
  %".25" = call float @"string.parse_float"(%"string" %"temp_mem.4")
  %".26" = call float @"float.mul_float"(float %".25", float %".25")
  store float %".26", float* %"area_ptr"
  br label %"cleanup"
elif_test_0:
  %".36" = call %"string" @"string.new"(i8* getelementptr ([10 x i8], [10 x i8]* @"str.4", i32 0, i32 0), i32 9)
  %".37" = extractvalue %"string" %".36", 2
  %".38" = call i8* @"Ref.inc"(%"Ref"* %".37")
  %"memory_var.5" = alloca %"string"
  store %"string" %".36", %"string"* %"memory_var.5"
  %"temp_mem.5" = load %"string", %"string"* %"memory_var.5"
  %".40" = call i1 @"string.eq_string"(%"string" %"temp_mem.1", %"string" %"temp_mem.5")
  br i1 %".40", label %"elif_then_0", label %"elif_test_1"
elif_then_0:
  %".42" = call %"string" @"string.new"(i8* getelementptr ([35 x i8], [35 x i8]* @"str.5", i32 0, i32 0), i32 34)
  %".43" = extractvalue %"string" %".42", 2
  %".44" = call i8* @"Ref.inc"(%"Ref"* %".43")
  %"memory_var.6" = alloca %"string"
  store %"string" %".42", %"string"* %"memory_var.6"
  %"temp_mem.6" = load %"string", %"string"* %"memory_var.6"
  %".46" = call %"string" @"input_prompt"(%"string" %"temp_mem.6")
  %".47" = extractvalue %"string" %".46", 2
  %".48" = call i8* @"Ref.inc"(%"Ref"* %".47")
  %"memory_var.7" = alloca %"string"
  store %"string" %".46", %"string"* %"memory_var.7"
  %"temp_mem.7" = load %"string", %"string"* %"memory_var.7"
  %".50" = call float @"string.parse_float"(%"string" %"temp_mem.7")
  %".51" = call %"string" @"string.new"(i8* getelementptr ([36 x i8], [36 x i8]* @"str.6", i32 0, i32 0), i32 35)
  %".52" = extractvalue %"string" %".51", 2
  %".53" = call i8* @"Ref.inc"(%"Ref"* %".52")
  %"memory_var.8" = alloca %"string"
  store %"string" %".51", %"string"* %"memory_var.8"
  %"temp_mem.8" = load %"string", %"string"* %"memory_var.8"
  %".55" = call %"string" @"input_prompt"(%"string" %"temp_mem.8")
  %".56" = extractvalue %"string" %".55", 2
  %".57" = call i8* @"Ref.inc"(%"Ref"* %".56")
  %"memory_var.9" = alloca %"string"
  store %"string" %".55", %"string"* %"memory_var.9"
  %"temp_mem.9" = load %"string", %"string"* %"memory_var.9"
  %".59" = call float @"string.parse_float"(%"string" %"temp_mem.9")
  %".60" = call float @"float.mul_float"(float %".50", float %".59")
  store float %".60", float* %"area_ptr"
  br label %"cleanup.1"
elif_test_1:
  %".76" = call %"string" @"string.new"(i8* getelementptr ([7 x i8], [7 x i8]* @"str.7", i32 0, i32 0), i32 6)
  %".77" = extractvalue %"string" %".76", 2
  %".78" = call i8* @"Ref.inc"(%"Ref"* %".77")
  %"memory_var.10" = alloca %"string"
  store %"string" %".76", %"string"* %"memory_var.10"
  %"temp_mem.10" = load %"string", %"string"* %"memory_var.10"
  %".80" = call i1 @"string.eq_string"(%"string" %"temp_mem.1", %"string" %"temp_mem.10")
  br i1 %".80", label %"elif_then_1", label %"if_else"
elif_then_1:
  %".82" = call %"string" @"string.new"(i8* getelementptr ([33 x i8], [33 x i8]* @"str.8", i32 0, i32 0), i32 32)
  %".83" = extractvalue %"string" %".82", 2
  %".84" = call i8* @"Ref.inc"(%"Ref"* %".83")
  %"memory_var.11" = alloca %"string"
  store %"string" %".82", %"string"* %"memory_var.11"
  %"temp_mem.11" = load %"string", %"string"* %"memory_var.11"
  %".86" = call %"string" @"input_prompt"(%"string" %"temp_mem.11")
  %".87" = extractvalue %"string" %".86", 2
  %".88" = call i8* @"Ref.inc"(%"Ref"* %".87")
  %"memory_var.12" = alloca %"string"
  store %"string" %".86", %"string"* %"memory_var.12"
  %"temp_mem.12" = load %"string", %"string"* %"memory_var.12"
  %".90" = call float @"string.parse_float"(%"string" %"temp_mem.12")
  %".91" = call float @"Math.pi"()
  %".92" = call float @"float.mul_float"(float %".90", float %".90")
  %".93" = call float @"float.mul_float"(float %".91", float %".92")
  store float %".93", float* %"area_ptr"
  br label %"cleanup.2"
if_else:
  %".103" = call %"string" @"string.new"(i8* getelementptr ([14 x i8], [14 x i8]* @"str.9", i32 0, i32 0), i32 13)
  %".104" = extractvalue %"string" %".103", 2
  %".105" = call i8* @"Ref.inc"(%"Ref"* %".104")
  %"memory_var.13" = alloca %"string"
  store %"string" %".103", %"string"* %"memory_var.13"
  %"temp_mem.13" = load %"string", %"string"* %"memory_var.13"
  %".107" = call i8* @"print_string"(%"string" %"temp_mem.13")
  br label %"cleanup.3"
cleanup:
  %".29" = getelementptr %"string", %"string"* %"memory_var.3", i32 0, i32 2
  %".30" = load %"Ref"*, %"Ref"** %".29"
  %".31" = call i8* @"Ref.dec"(%"Ref"* %".30")
  %".32" = getelementptr %"string", %"string"* %"memory_var.4", i32 0, i32 2
  %".33" = load %"Ref"*, %"Ref"** %".32"
  %".34" = call i8* @"Ref.dec"(%"Ref"* %".33")
  br label %"if_merge"
cleanup.1:
  %".63" = getelementptr %"string", %"string"* %"memory_var.6", i32 0, i32 2
  %".64" = load %"Ref"*, %"Ref"** %".63"
  %".65" = call i8* @"Ref.dec"(%"Ref"* %".64")
  %".66" = getelementptr %"string", %"string"* %"memory_var.7", i32 0, i32 2
  %".67" = load %"Ref"*, %"Ref"** %".66"
  %".68" = call i8* @"Ref.dec"(%"Ref"* %".67")
  %".69" = getelementptr %"string", %"string"* %"memory_var.8", i32 0, i32 2
  %".70" = load %"Ref"*, %"Ref"** %".69"
  %".71" = call i8* @"Ref.dec"(%"Ref"* %".70")
  %".72" = getelementptr %"string", %"string"* %"memory_var.9", i32 0, i32 2
  %".73" = load %"Ref"*, %"Ref"** %".72"
  %".74" = call i8* @"Ref.dec"(%"Ref"* %".73")
  br label %"if_merge"
cleanup.2:
  %".96" = getelementptr %"string", %"string"* %"memory_var.11", i32 0, i32 2
  %".97" = load %"Ref"*, %"Ref"** %".96"
  %".98" = call i8* @"Ref.dec"(%"Ref"* %".97")
  %".99" = getelementptr %"string", %"string"* %"memory_var.12", i32 0, i32 2
  %".100" = load %"Ref"*, %"Ref"** %".99"
  %".101" = call i8* @"Ref.dec"(%"Ref"* %".100")
  br label %"if_merge"
cleanup.3:
  %".109" = getelementptr %"string", %"string"* %"memory_var.13", i32 0, i32 2
  %".110" = load %"Ref"*, %"Ref"** %".109"
  %".111" = call i8* @"Ref.dec"(%"Ref"* %".110")
  br label %"if_merge"
cleanup.4:
  %".127" = getelementptr %"string", %"string"* %"memory_var", i32 0, i32 2
  %".128" = load %"Ref"*, %"Ref"** %".127"
  %".129" = call i8* @"Ref.dec"(%"Ref"* %".128")
  %".130" = getelementptr %"string", %"string"* %"memory_var.1", i32 0, i32 2
  %".131" = load %"Ref"*, %"Ref"** %".130"
  %".132" = call i8* @"Ref.dec"(%"Ref"* %".131")
  %".133" = extractvalue %"string" %"temp_mem.1", 2
  %".134" = call i8* @"Ref.dec"(%"Ref"* %".133")
  %".135" = getelementptr %"string", %"string"* %"memory_var.2", i32 0, i32 2
  %".136" = load %"Ref"*, %"Ref"** %".135"
  %".137" = call i8* @"Ref.dec"(%"Ref"* %".136")
  %".138" = getelementptr %"string", %"string"* %"memory_var.5", i32 0, i32 2
  %".139" = load %"Ref"*, %"Ref"** %".138"
  %".140" = call i8* @"Ref.dec"(%"Ref"* %".139")
  %".141" = getelementptr %"string", %"string"* %"memory_var.10", i32 0, i32 2
  %".142" = load %"Ref"*, %"Ref"** %".141"
  %".143" = call i8* @"Ref.dec"(%"Ref"* %".142")
  %".144" = getelementptr %"string", %"string"* %"memory_var.14", i32 0, i32 2
  %".145" = load %"Ref"*, %"Ref"** %".144"
  %".146" = call i8* @"Ref.dec"(%"Ref"* %".145")
  %".147" = getelementptr %"string", %"string"* %"memory_var.15", i32 0, i32 2
  %".148" = load %"Ref"*, %"Ref"** %".147"
  %".149" = call i8* @"Ref.dec"(%"Ref"* %".148")
  %".150" = getelementptr %"string", %"string"* %"memory_var.16", i32 0, i32 2
  %".151" = load %"Ref"*, %"Ref"** %".150"
  %".152" = call i8* @"Ref.dec"(%"Ref"* %".151")
  br label %"return"
return:
  ret i32 0
}

@"str" = internal constant [47 x i8] c"What shape do you want to find the area of?\0a> \00"
define %"string" @"string.new"(i8* %".1", i32 %".2")
{
.4:
  %".5" = zext i32 %".2" to i64
  %".6" = add i64 %".5", 1
  %".7" = call i8* @"malloc"(i64 %".6")
  %".8" = call i8* @"memcpy"(i8* %".7", i8* %".1", i64 %".5")
  %".9" = getelementptr i8, i8* %".7", i64 %".5"
  store i8 0, i8* %".9"
  %".11" = call %"Ref"* @"Ref.new"(i8* %".7", i8* (i8*)* null)
  %".12" = insertvalue %"string" undef, i8* %".7", 0
  %".13" = insertvalue %"string" %".12", i64 %".5", 1
  %".14" = insertvalue %"string" %".13", %"Ref"* %".11", 2
  ret %"string" %".14"
}

declare i8* @"malloc"(i64 %".1")

declare i8* @"memcpy"(i8* %".1", i8* %".2", i64 %".3")

define %"Ref"* @"Ref.new"(i8* %".1", i8* (i8*)* %".2")
{
.4:
  %".5" = getelementptr %"Ref", %"Ref"* null, i32 1
  %".6" = ptrtoint %"Ref"* %".5" to i64
  %".7" = call i8* @"malloc"(i64 %".6")
  %".8" = bitcast i8* %".7" to %"Ref"*
  %".9" = getelementptr %"Ref", %"Ref"* %".8", i32 0, i32 0
  store i8* %".1", i8** %".9"
  %".11" = getelementptr %"Ref", %"Ref"* %".8", i32 0, i32 1
  store i8* (i8*)* %".2", i8* (i8*)** %".11"
  %".13" = getelementptr %"Ref", %"Ref"* %".8", i32 0, i32 2
  store i64 1, i64* %".13"
  ret %"Ref"* %".8"
}

define i8* @"Ref.inc"(%"Ref"* %".1")
{
.3:
  %".4" = getelementptr %"Ref", %"Ref"* %".1", i32 0, i32 2
  %".5" = load i64, i64* %".4"
  %".6" = add i64 %".5", 1
  store i64 %".6", i64* %".4"
  ret i8* null
}

define %"string" @"input_prompt"(%"string" %".1")
{
.3:
  %".4" = extractvalue %"string" %".1", 0
  %".5" = call i32 (i8*, ...) @"printf"(i8* getelementptr ([3 x i8], [3 x i8]* @"str.1", i32 0, i32 0), i8* %".4")
  %".6" = call %"string" @"input"()
  ret %"string" %".6"
}

declare i32 @"printf"(i8* %".1", ...)

@"str.1" = internal constant [3 x i8] c"%s\00"
define %"string" @"input"()
{
.2:
  %".3" = call {i8*} @"__acrt_iob_func"(i32 0)
  %".4" = call i8* @"fgets"(i8* getelementptr ([256 x i8], [256 x i8]* @".1", i32 0, i32 0), i32 256, {i8*} %".3")
  %".5" = call i64 @"strlen"(i8* getelementptr ([256 x i8], [256 x i8]* @".1", i32 0, i32 0))
  %".6" = sub i64 %".5", 1
  %".7" = getelementptr i8, i8* getelementptr ([256 x i8], [256 x i8]* @".1", i32 0, i32 0), i64 %".6"
  %".8" = load i8, i8* %".7"
  %".9" = icmp eq i8 %".8", 10
  br i1 %".9", label %".2.if", label %".2.endif"
.2.if:
  store i8 0, i8* %".7"
  %".12" = sub i64 %".5", 1
  br label %".2.endif"
.2.endif:
  %".14" = trunc i64 %".12" to i32
  %".15" = call %"string" @"string.new"(i8* getelementptr ([256 x i8], [256 x i8]* @".1", i32 0, i32 0), i32 %".14")
  ret %"string" %".15"
}

declare i64 @"strlen"(i8* %".1")

declare i8* @"fgets"(i8* %".1", i32 %".2", {i8*} %".3")

@".1" = internal global [256 x i8] zeroinitializer
declare {i8*} @"__acrt_iob_func"(i32 %".1")

@"str.2" = internal constant [7 x i8] c"square\00"
define i1 @"string.eq_string"(%"string" %".1", %"string" %".2")
{
.4:
  %".5" = extractvalue %"string" %".1", 1
  %".6" = extractvalue %"string" %".2", 1
  %".7" = icmp ne i64 %".5", %".6"
  br i1 %".7", label %".4.if", label %".4.endif"
.4.if:
  ret i1 0
.4.endif:
  %".10" = extractvalue %"string" %".1", 0
  %".11" = extractvalue %"string" %".2", 0
  %".12" = call i1 @"memcmp"(i8* %".10", i8* %".11", i64 %".5")
  %".13" = icmp eq i1 %".12", 0
  ret i1 %".13"
}

declare i1 @"memcmp"(i8* %".1", i8* %".2", i64 %".3")

@"str.3" = internal constant [31 x i8] c"Enter the length of one side: \00"
define float @"string.parse_float"(%"string" %".1")
{
.3:
  %".4" = extractvalue %"string" %".1", 0
  %".5" = call double @"strtod"(i8* %".4", i8* null)
  %".6" = fptrunc double %".5" to float
  ret float %".6"
}

declare double @"strtod"(i8* %".1", i8* %".2")

define float @"float.mul_float"(float %".1", float %".2")
{
.4:
  %".5" = fmul float %".1", %".2"
  ret float %".5"
}

define i8* @"Ref.dec"(%"Ref"* %".1")
{
.3:
  %".4" = getelementptr %"Ref", %"Ref"* %".1", i32 0, i32 2
  %".5" = load i64, i64* %".4"
  %".6" = sub i64 %".5", 1
  store i64 %".6", i64* %".4"
  %".8" = icmp eq i64 %".6", 0
  br i1 %".8", label %".3.if", label %".3.endif"
.3.if:
  %".10" = getelementptr %"Ref", %"Ref"* %".1", i32 0, i32 0
  %".11" = load i8*, i8** %".10"
  %".12" = getelementptr %"Ref", %"Ref"* %".1", i32 0, i32 1
  %".13" = load i8* (i8*)*, i8* (i8*)** %".12"
  %".14" = icmp ne i8* (i8*)* %".13", null
  br i1 %".14", label %".3.if.if", label %".3.if.else"
.3.endif:
  ret i8* null
.3.if.if:
  %".16" = call i8* %".13"(i8* %".11")
  br label %".3.if.endif"
.3.if.else:
  call void @"free"(i8* %".11")
  br label %".3.if.endif"
.3.if.endif:
  store i8* null, i8** %".10"
  %".21" = bitcast %"Ref"* %".1" to i8*
  call void @"free"(i8* %".21")
  br label %".3.endif"
}

declare void @"free"(i8* %".1")

@"str.4" = internal constant [10 x i8] c"rectangle\00"
@"str.5" = internal constant [35 x i8] c"Enter the width of the rectangle: \00"
@"str.6" = internal constant [36 x i8] c"Enter the height of the rectangle: \00"
@"str.7" = internal constant [7 x i8] c"circle\00"
@"str.8" = internal constant [33 x i8] c"Enter the radius of the circle: \00"
define float @"Math.pi"()
{
.2:
  ret float 0x400921fb60000000
}

@"str.9" = internal constant [14 x i8] c"Unknown shape\00"
define i8* @"print_string"(%"string" %".1")
{
.3:
  %".4" = call %"string" @"string.to_string"(%"string" %".1")
  %".5" = extractvalue %"string" %".4", 0
  %".6" = call i32 @"puts"(i8* %".5")
  %".7" = extractvalue %"string" %".4", 2
  %".8" = call i8* @"Ref.dec"(%"Ref"* %".7")
  ret i8* null
}

declare i32 @"puts"(i8* %".1")

define %"string" @"string.to_string"(%"string" %".1")
{
.3:
  ret %"string" %".1"
}

@"str.10" = internal constant [7 x i8] c"Area: \00"
define %"string" @"float.to_string"(float %".1")
{
.3:
  %".4" = call i32 (i8*, i64, i8*, ...) @"snprintf"(i8* getelementptr ([64 x i8], [64 x i8]* @".2", i32 0, i32 0), i64 64, i8* getelementptr ([3 x i8], [3 x i8]* @"str.11", i32 0, i32 0), float %".1")
  %".5" = trunc i64 64 to i32
  %".6" = call %"string" @"string.new"(i8* getelementptr ([64 x i8], [64 x i8]* @".2", i32 0, i32 0), i32 %".5")
  ret %"string" %".6"
}

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

@".2" = internal global [64 x i8] zeroinitializer
@"str.11" = internal constant [3 x i8] c"%f\00"
define %"string" @"string.add_string"(%"string" %".1", %"string" %".2")
{
.4:
  %".5" = extractvalue %"string" %".1", 1
  %".6" = extractvalue %"string" %".2", 1
  %".7" = add i64 %".5", %".6"
  %".8" = add i64 %".7", 1
  %".9" = call i8* @"malloc"(i64 %".8")
  %".10" = extractvalue %"string" %".1", 0
  %".11" = extractvalue %"string" %".2", 0
  %".12" = call i8* @"memcpy"(i8* %".9", i8* %".10", i64 %".5")
  %".13" = getelementptr i8, i8* %".9", i64 %".5"
  %".14" = call i8* @"memcpy"(i8* %".13", i8* %".11", i64 %".6")
  %".15" = getelementptr i8, i8* %".9", i64 %".7"
  store i8 0, i8* %".15"
  %".17" = trunc i64 %".7" to i32
  %".18" = call %"string" @"string.new"(i8* %".9", i32 %".17")
  ret %"string" %".18"
}
