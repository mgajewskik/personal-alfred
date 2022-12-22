data "aws_route53_zone" "domain" {
  name         = var.base_domain
  private_zone = false
}

resource "aws_acm_certificate" "cert" {
  domain_name       = "${var.service_name}.${var.base_domain}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "verify" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.domain.zone_id
}

resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.verify : record.fqdn]
}

output "domain_name" {
  value = aws_acm_certificate.cert.domain_name
}

output "certificate_arn" {
  value = aws_acm_certificate_validation.cert.certificate_arn
}
