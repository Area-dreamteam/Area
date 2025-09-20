import { Controller, Post, Body, Get, UseGuards, Request } from '@nestjs/common';
import { AuthService } from './auth.service';
import { RegisterDto } from './dto/register.dto';
import { LoginDto } from './dto/login.dto';
import { ApiTags, ApiBearerAuth, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { Role } from '../common/enum/role.enum';
import { JwtAuthGuard } from '../common/guards/jwtAuth.guard';
import { Public } from '../common/decorators/public.decorator'

@Public()
@ApiTags('auth')
@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @Post('register')
  @ApiOperation({ summary: 'Create new user' })
  @ApiResponse({ status: 201 })
  async register(@Body() dto: RegisterDto) {
    return this.authService.register(dto.email, dto.username, dto.password, Role.User);
  }

  @Post('login')
  @UseGuards(JwtAuthGuard)
  @ApiOperation({ summary: 'connect to account' })
  @ApiResponse({ status: 200 })
  async login(@Body() dto: LoginDto) {
    return this.authService.login(dto.email, dto.password);
  }
}
