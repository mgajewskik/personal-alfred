variable "filename" {
  type = string
}

variable "resource_prefix" {
  type = string
}

variable "name" {
  type = string
}

variable "handler" {
  type = string
}

variable "memory_size" {
  type = number
}

variable "env" {
  type = map(string)
}

variable "layers" {
  type = list(string)
}

variable "permissions" {
  type = list(string)
}
