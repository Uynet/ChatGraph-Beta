#version 330 core

uniform float time;
in vec2 uv;
out vec4 fragColor;
// in vec3 vertexPosition;

float lineDist(vec2 p, vec2 start, vec2 end, float width)
{
	vec2 dir = start - end;
	float lngth = length(dir);
	dir /= lngth;
	vec2 proj = max(0.0, min(lngth, dot((start - p), dir))) * dir;
	return length( (start - p) - proj ) - (width / 2.0);
}


void main() {
    // uv and line (0,0 to 1,1)
    vec2 p = uv;
    vec2 start = vec2(0.0,0.0);
    vec2 end= vec2(1.0,1.0);
    float width = 0.1;
    float d = lineDist(p , start , end , width);

    /// wave width 
    float v = 3.0;
    float lam = 50.0;
    float a = 3.0;
    float s = a *  sin(uv.x * lam + time * v);
    vec3 c = vec3(0.2 , 0.2 , 0.2);
    c *= s;
    fragColor = vec4(c, 1.0);
}